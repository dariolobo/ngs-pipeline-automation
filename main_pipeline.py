import argparse
import sys
from pathlib import Path

# Import core execution functions from each module
from modules.module_1_qc_filter import run_quality_filter
from modules.module_2_alignment import run_alignment
from modules.module_3_post_processing import run_post_processing
from modules.module_4_reporting import run_reporting

def main():
    parser = argparse.ArgumentParser(
        description="NGS Automated Pipeline: From Raw FASTQ to Multi QC Report"
    )
    parser.add_argument("-1", "--read1", required=True, help="Path to Raw R1 FASTQ file")
    parser.add_argument("-2", "--read2", required=True, help="Path to Raw R2 FASTQ file")
    parser.add_argument("-x", "--index", required=True, help="Path prefix to reference genome index")
    parser.add_argument("-o", "--outdir", default="pipeline_results", help="Main output directory")
    parser.add_argument("-t", "--threads", type=int, default=4, help="CPU threads to use (default: 4)")

    args = parser.parse_args()

    main_out = Path(args.outdir)
    main_out.mkdir(parents=True, exist_ok=True)

    print("-" * 60)
    print("STARTING AUTOMATED NGS PIPELINE")
    print("-" * 60)

    # Step 1: Quality Control & Filtering
    print("\n[STEP 1/4] Running Quality Control & Filtering...")
    qc_dir = main_out / "01_qc"
    clean_r1, clean_r2 = run_quality_filter(
        read1=args.read1,
        read2=args.read2,
        output_dir=str(qc_dir)
    )

    # Step 2: Genome Alignment
    print("\n[STEP 2/4] Running Genome Alignment...")
    align_dir = main_out / "02_alignment"
    sam_file = run_alignment(
        read1=str(clean_r1),
        read2=str(clean_r2),
        index_prefix=args.index,
        output_dir=str(align_dir),
        threads=args.threads
    )

    # Step 3: SAM to Sorted BAM Processing
    print("\n[STEP 3/4] Running SAM to Sorted BAM Processing...")
    bam_dir = main_out / "03_processed_bam"
    sorted_bam = run_post_processing(
        sam_file=str(sam_file),
        output_dir=str(bam_dir),
        threads=args.threads
    )

    # Step 4: Consolidated MultiQC Report Generation
    print("\n[STEP 4/4] Generating Consolidated MultiQC Report...")
    report_dir = main_out / "04_reports"
    run_reporting(
        input_dir=str(main_out),
        output_dir=str(report_dir)
    )

    print("\n" + "-" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"All results stored in: {main_out.resolve()}")
    print("-" * 60)

if __name__ == "__main__":
    main()