#!/bin/bash
# Bash script that checks all the mp4 files in a folder and executes a python script command
# Make the script executable with
    # chmod +x process_mp4_files.sh
# Ensure that requirements.txt packages are correctly installed in a virtual environment
# Run the virtual environment
# Execute the script with $ ./process_mp4_files.sh to generate the keypoints for the videos frames
python_script="keypoints.py"
root_folder="videos/"
keypoints_file_extension="points"

find "$root_folder" -name "*.mp4" | while IFS= read -r file; do
    if [ -f "$file" ]; then
        folder_path=$(dirname "$file")
        output_folder="$folder_path/output"
        
        echo "Processing: $file"
        
        mkdir -p "$output_folder"

        # Append 0s to the file name
        filename=$(basename "$file")
        filename_with_zeros=$(printf "%08s" "$filename" | tr ' ' '0')
        output_filename="$output_folder/$filename_with_zeros.$keypoints_file_extension"

        python "$python_script" -i "$file" -b False -k "$output_filename" -m 1
    fi
done

