import argparse
import subprocess
import sys
from pathlib import Path

def run_command(cmd: str) -> str:
    """
    Executes a system shell command and handles execution errors.
    """
    print(f"[EXEC]: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode !=0:
        print(f"[ERROR]: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout

def run_post_processing(sam_file: str, output_dir: str, threads: int = 4) -> Path:
    """
    Converts SAM to sorted BAM and generates a BAM index (.bai) using Samtools.

    Returns:
        Path: Path to the sorted BAM file.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    sorted_bam = out_path / "aligned_sorted.bam"

    # Step 1: Convert SAM to sorted BAM directly
    sort_cmd = f"samtools sort -@{threads} -o {sorted_bam} {sam_file}"
    run_command(sort_cmd)

    # Step 2: Index the sorted BAM file
    index_cmd = f"samtools index {sorted_bam}"
    run_command(index_cmd)

    print(f"[SUCCESS] Module 3 completed. Sorted BAM and index created at: {sorted_bam}")

    return sorted_bam

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Module 3: SAM to Sorted BAM Conversion & Indexing"
    )
    parser.add_argument("-s", "--sam", required=True, help="Path to input SAM file")
    parser.add_argument("-o", "--outdir", default="03_post_processing_output", help="Output directory")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of CPU threads to use (defaul:4)")

    args = parser.parse_args()
    run_post_processing(args.sam, args.outdir, args.threads)