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
    if result.returncode != 0:
        print(f"[ERROR]: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout

def run_alignment(
        read1: str,
        read2: str,
        index_prefix: str,
        output_dir: str,
        threads: int = 4
) -> Path:
    """
    Aligns paired-end reads to a reference genome using HISAT2.

    Returns:
        Path: Path to the output alignment SAM file.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    sam_file = out_path / "aligned_reads.sam"

    # Command for paired-end genome alignment using HISAT2
    alignment_cmd = (
        f"hisat2 -p {threads} "
        f"-x {index_prefix} "
        f" -1 {read1} -2 {read2} "
        f"-S {sam_file}"
    )

    run_command(alignment_cmd)
    print(f"[SUCCESS] Module 2 completed. SAM file generated at: {sam_file}")

    return sam_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Module 2: Automated NGS Genome Alignment using HISAT2"
    )
    parser.add_argument("-1", "--read1", required=True, help="Path to clean R1 FASTQ file")
    parser.add_argument("-2", "--read2", required=True, help="Path to clean R2 FASTQ file")
    parser.add_argument("-x", "--index", required=True, help="Path prefix to reference genome index")
    parser.add_argument("-o", "--outdir", default="02_alignment_output", help="Output directory")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of CPU threads to use (default:4)")


    args = parser.parse_args()
    run_alignment(args.read1, args.read2, args.index, args.outdir, args.threads)
