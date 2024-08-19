import os
import subprocess
import sys
import filecmp
import time

def compile_java(java_file):
    try:
        subprocess.check_call(['javac', java_file])
        print(f"Compiled {java_file} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling {java_file}: {e}")
        sys.exit(1)

def run_java_class(class_name, input_file):
    start_time = time.perf_counter()
    try:
        with open(input_file, 'r') as infile, open('output.txt', 'w') as outfile:
            subprocess.check_call(['java', class_name], stdin=infile, stdout=outfile)
    except subprocess.CalledProcessError as e:
        print(f"Error running {class_name}: {e}")
        sys.exit(1)
    end_time = time.perf_counter()
    return end_time - start_time 

def compare_output(output_file, expected_output_file):
    return filecmp.cmp(output_file, expected_output_file, shallow=False)

def main(java_file, input_output_folder):
    # Compile the Java file
    compile_java(java_file)

    class_name = os.path.splitext(os.path.basename(java_file))[0]
    
    input_files = sorted([f for f in os.listdir(input_output_folder) if f.endswith('.in')])
    output_files = sorted([f for f in os.listdir(input_output_folder) if f.endswith('.ans')])
    
    if len(input_files) != len(output_files):
        print("Number of .in files and .out files do not match.")
        sys.exit(1)

    for input_file, output_file in zip(input_files, output_files):
        input_path = os.path.join(input_output_folder, input_file)
        expected_output_path = os.path.join(input_output_folder, output_file)

        # Run the Java class with the input file
        exe_time = run_java_class(class_name, input_path)
        
            # Compare the output with the expected output
        if compare_output('output.txt', expected_output_path):
            print(f"Test {input_file} passed.")
        else:
            print(f"Test {input_file} failed.")
        print(f"Time Taken(s): {exe_time}")
        # with open('output.txt', 'r') as outfile:
            #    print("Output:\n", outfile.read()) 
            #with open(expected_output_path, 'r') as expectedfile:
            #    print("Expected:\n", expectedfile.read())
    
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run_tests.py <JavaFile.java> <InputOutputFolder>")
        sys.exit(1)

    java_file = sys.argv[1]
    input_output_folder = sys.argv[2]

    main(java_file, input_output_folder)