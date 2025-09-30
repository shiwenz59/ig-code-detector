import cv2
import os
import sys
from pathlib import Path

def extract_frames_from_video(video_path, output_dir, frames_per_minute=5):
    """
    Extract frames from a video at a specified rate.
    
    Args:
        video_path (str): Path to the input video file
        output_dir (str): Directory to save extracted frames
        frames_per_minute (int): Number of frames to extract per minute (default: 5)
    
    Returns:
        dict: Summary of extraction results
    """
    # Validate input file
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_seconds = total_frames / fps if fps > 0 else 0
    
    print(f"Video Properties:")
    print(f"  - FPS: {fps:.2f}")
    print(f"  - Total Frames: {total_frames}")
    print(f"  - Duration: {duration_seconds:.2f} seconds ({duration_seconds/60:.2f} minutes)")
    print(f"  - Extracting {frames_per_minute} frames per minute")
    print()
    
    # Calculate frame interval
    frames_per_second = frames_per_minute / 60
    frame_interval = int(fps / frames_per_second) if frames_per_second > 0 else 1
    
    print(f"Extracting 1 frame every {frame_interval} frames ({60/frames_per_minute:.1f} seconds)")
    print()
    
    # Extract frames
    frame_count = 0
    extracted_count = 0
    
    video_filename = Path(video_path).stem
    
    print("Extracting frames...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            # Generate output filename with timestamp
            timestamp_seconds = frame_count / fps
            output_filename = f"{video_filename}_frame_{extracted_count:04d}_t{timestamp_seconds:.2f}s.jpg"
            output_path = os.path.join(output_dir, output_filename)
            
            # Save frame
            cv2.imwrite(output_path, frame)
            extracted_count += 1
            
            if extracted_count % 10 == 0:
                print(f"  Extracted {extracted_count} frames...")
        
        frame_count += 1
    
    cap.release()
    
    print()
    print(f"✓ Extraction complete!")
    print(f"  - Total frames extracted: {extracted_count}")
    print(f"  - Frames saved to: {output_dir}")
    
    return {
        "video_path": video_path,
        "output_dir": output_dir,
        "fps": fps,
        "duration_seconds": duration_seconds,
        "total_frames": total_frames,
        "frames_extracted": extracted_count,
        "frames_per_minute": frames_per_minute
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python frame_extractor_demo.py <video_path> [frames_per_minute] [output_dir]")
        print()
        print("Arguments:")
        print("  video_path         Path to the video file (required)")
        print("  frames_per_minute  Number of frames to extract per minute (default: 5)")
        print("  output_dir         Directory to save frames (default: ./extracted_frames)")
        print()
        print("Example:")
        print("  python frame_extractor_demo.py video.mp4 10 ./frames")
        sys.exit(1)
    
    video_path = sys.argv[1]
    frames_per_minute = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "./extracted_frames"
    
    try:
        result = extract_frames_from_video(video_path, output_dir, frames_per_minute)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()