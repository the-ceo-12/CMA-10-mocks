#!/usr/bin/env python3
"""
CMA Practice PDF Parser
Usage: python parse_pdf.py <path_to_pdf>
Outputs: questions.json in the same directory as this script
"""

import re
import json
import sys
import subprocess
import os

def extract_text(pdf_path):
    """Extract text from PDF using pdftotext"""
    result = subprocess.run(
        ['pdftotext', pdf_path, '-'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error extracting text: {result.stderr}")
        sys.exit(1)
    return result.stdout

def parse_questions(test_text):
    """Parse questions from a test block"""
    questions = []
    test_text = test_text.replace('\f', '\n')
    
    # Split on Question #N:
    qblocks = re.split(r'Question #(\d+):', test_text)
    
    i = 1
    while i < len(qblocks) - 1:
        q_num = qblocks[i].strip()
        q_body = qblocks[i + 1]
        
        # Check for Fact Pattern
        fact_pattern = ""
        fp_match = re.search(r'Fact Pattern[:\s]+(.*?)(?=(?:Question:|^[A-D]\.|\nA\.))', q_body, re.DOTALL | re.MULTILINE)
        if fp_match:
            fact_pattern = fp_match.group(1).strip()[:1500]
            q_body = q_body[fp_match.end():]
            q_body = re.sub(r'^Question:\s*', '', q_body.lstrip())

        # Also handle inline fact patterns like "[Fact Pattern]"
        bracket_fp = re.search(r'\[Fact Pattern[^\]]*\](.*?)(?=(?:Question:|^[A-D]\.|\nA\.))', q_body, re.DOTALL | re.MULTILINE)
        if bracket_fp and not fact_pattern:
            fact_pattern = bracket_fp.group(1).strip()[:1500]
            q_body = q_body[bracket_fp.end():]
            q_body = re.sub(r'^Question:\s*', '', q_body.lstrip())

        # Extract question text (everything before first "A." option)
        q_match = re.match(r'(.*?)(?=\n[A-D]\.\s)', q_body, re.DOTALL)
        if not q_match:
            i += 2
            continue
        q_text = q_match.group(1).strip()
        
        # Remove "Correct Answer" hints that sometimes appear
        q_text = re.sub(r'Correct Answer[:\s•]+.*', '', q_text, flags=re.DOTALL).strip()
        q_text = re.sub(r'All Possible Answers[:\s]*$', '', q_text).strip()
        
        rest = q_body[q_match.end():]
        
        # Extract options A, B, C, D
        option_matches = re.findall(r'\n([A-D])\.\s*(.*?)(?=\n[A-D]\.|Explanation:|$)', rest, re.DOTALL)
        options = {}
        for letter, text in option_matches:
            clean = text.strip()
            clean = re.sub(r'Correct Answer[:\s•]+.*', '', clean, flags=re.DOTALL).strip()
            clean = re.sub(r'All Possible Answers[:\s]*$', '', clean).strip()
            options[letter] = clean
        
        # Extract correct answer
        correct = None
        # Method 1: "Answer (X) is correct."
        correct_match = re.search(r'Answer\s*\(([A-D])\)\s+is correct', rest, re.IGNORECASE)
        if correct_match:
            correct = correct_match.group(1).upper()
        
        # Method 2: "Correct Answer: X." or "Correct Answer • X"
        if not correct:
            ca_match = re.search(r'Correct Answer[:\s•]+([A-D])[\.\s]', q_body + rest)
            if ca_match:
                correct = ca_match.group(1).upper()
        
        # Extract explanation (try to get the correct answer's explanation)
        explanation = ""
        exp_section = re.search(r'Explanation:(.*?)$', rest, re.DOTALL)
        if exp_section:
            exp_text = exp_section.group(1).strip()
            # Find the correct answer explanation
            if correct:
                # Try labeled "Answer (X) is correct." block
                correct_exp = re.search(
                    rf'Answer\s*\({correct}\)\s+is correct\.(.*?)(?=Answer\s*\([A-D]\)|$)',
                    exp_text, re.DOTALL | re.IGNORECASE
                )
                if correct_exp:
                    explanation = correct_exp.group(1).strip()[:600]
                else:
                    explanation = exp_text[:600]
            else:
                explanation = exp_text[:600]
        
        if options and correct and len(options) >= 2:
            questions.append({
                "num": int(q_num) if q_num.isdigit() else len(questions) + 1,
                "factPattern": fact_pattern,
                "text": q_text[:800],
                "options": options,
                "correct": correct,
                "explanation": explanation
            })
        
        i += 2
    
    return questions

def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_pdf.py <path_to_pdf>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        sys.exit(1)
    
    print(f"Extracting text from {pdf_path}...")
    text = extract_text(pdf_path)
    
    # Clean form feeds
    text = text.replace('\f', '\n')
    
    print("Parsing mock tests...")
    # Split by test boundaries
    parts = re.split(r'(?:CMA PASS )?MOCK TEST (\d+)', text)
    
    all_tests = {}
    total_q = 0
    
    for idx in range(1, len(parts) - 1, 2):
        test_num = parts[idx].strip()
        test_body = parts[idx + 1]
        questions = parse_questions(test_body)
        test_key = f"Mock Test {test_num}"
        all_tests[test_key] = questions
        total_q += len(questions)
        print(f"  {test_key}: {len(questions)} questions parsed")
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'questions.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_tests, f, ensure_ascii=False, indent=2)
    
    print(f"\nDone! {total_q} questions saved to {output_path}")
    print(f"JSON size: {os.path.getsize(output_path) / 1024:.0f} KB")

if __name__ == '__main__':
    main()
