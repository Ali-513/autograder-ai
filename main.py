import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.autograder_ai.engine import EvaluationEngine

def process_student(student_path: Path, assignment_path: Path):
    print(f"\n🚀 Processing {student_path.name}")

    engine = EvaluationEngine(
        assignment_path=assignment_path,
        submission_path=student_path
    )

    results = engine.run()
    report = engine.generate_report()

    return student_path.name, results, report

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Autograder tool: provide assignment PDF and student submission."
    )

    parser.add_argument(
        "--assignment",
        required=True,
        type=Path,
        help="Path to the assignment PDF file.",
    )

    parser.add_argument(
        "--submission",
        required=True,
        type=Path,
        help="Path to the student's code submission file or directory.",
    )

    return parser.parse_args()


def validate_paths(assignment: Path, submission: Path):
    """Check if provided files/folders exist."""
    if not assignment.exists():
        print(f"Assignment file not found: {assignment}")
        sys.exit(1)

    if not submission.exists():
        print(f"Submission path not found: {submission}")
        sys.exit(1)


# def main():
#     load_dotenv()

#     args = parse_args()
#     validate_paths(args.assignment, args.submission)

#     engine = EvaluationEngine(args.assignment, args.submission)

#     results = engine.run()
#     print(engine.generate_report())
def main():
    load_dotenv()

    args = parse_args()
    validate_paths(args.assignment, args.submission)
    student_dirs = [d for d in args.submission.iterdir() if d.is_dir()]
    # 🔍 Detect if multiple student folders exist
    if student_dirs:
        print(f"\n📂 Detected {len(student_dirs)} student submissions.")
        all_results = {}

        # 🔥 CONCURRENCY HERE
        with ThreadPoolExecutor(max_workers=min(3, len(student_dirs))) as executor:
            futures = {
                executor.submit(process_student, student_dir, args.assignment): student_dir
                for student_dir in student_dirs
            }

            for future in as_completed(futures):
                student_dir = futures[future]

                try:
                    name, results, report = future.result()
                    all_results[name] = results

                    print("\n" + "=" * 80)
                    print(f"📊 REPORT FOR: {name}")
                    print("=" * 80)
                    print(report)
                    print(f"\n✅ Completed: {name}")

                except Exception as e:
                    print(f"\n❌ Failed: {student_dir.name} -> {e}")

    else:
        print("\n📄 Single submission mode")

        engine = EvaluationEngine(args.assignment, args.submission)

        results = engine.run()
        print("\n" + "=" * 80)
        print(f"📊 REPORT FOR: {args.submission.name}")
        print("=" * 80)
        print(engine.generate_report())


if __name__ == "__main__":
    main()
