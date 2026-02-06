import os
import re
import argparse

def delete_checkpoints_between(folder, t_start, t_end, dry_run=False):
    # regex to capture the timestamp at the end of the filename
    pattern = re.compile(r"net_weights_epoch_\d+_(\d+)\.pth")

    deleted = []

    for fname in os.listdir(folder):
        match = pattern.fullmatch(fname)
        if not match:
            continue

        timestamp = int(match.group(1))

        if t_start < timestamp < t_end:
            full_path = os.path.join(folder, fname)
            deleted.append(fname)

            if not dry_run:
                os.remove(full_path)

    return deleted


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Delete checkpoint files whose timestamps fall between two values"
    )
    parser.add_argument("folder", help="Path to checkpoint folder")
    parser.add_argument("start_ts", type=int, help="Start timestamp (exclusive)")
    parser.add_argument("end_ts", type=int, help="End timestamp (exclusive)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which files would be deleted without deleting them"
    )

    args = parser.parse_args()

    deleted = delete_checkpoints_between(
        args.folder, args.start_ts, args.end_ts, args.dry_run
    )

    if args.dry_run:
        print("Dry run — files that would be deleted:")
    else:
        print("Deleted files:")

    for f in deleted:
        print(" ", f)

    print(f"\nTotal: {len(deleted)} files")
