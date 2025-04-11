from flask import Flask, render_template, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "")
    user_input = data.get("input", "")

    filename = f"temp_{uuid.uuid4()}"
    ext_map = {
        "python": ".py",
        "c": ".c",
        "cpp": ".cpp",
        "java": ".java"
    }

    ext = ext_map.get(language)
    if not ext:
        return jsonify({"error": "Unsupported language."})

    filepath = f"{filename}{ext}"

    with open(filepath, "w") as f:
        f.write(code)

    try:
        if language == "python":
            result = subprocess.run(["python", filepath], input=user_input, capture_output=True, text=True, timeout=5)

        elif language == "c":
            output_exec = f"{filename}.exe" if os.name == "nt" else filename
            compile = subprocess.run(["gcc", filepath, "-o", output_exec], capture_output=True, text=True)
            if compile.returncode != 0:
                return jsonify({"output": compile.stderr})
            result = subprocess.run([output_exec], input=user_input, capture_output=True, text=True, timeout=5)

        elif language == "cpp":
            output_exec = f"{filename}.exe" if os.name == "nt" else filename
            compile = subprocess.run(["g++", filepath, "-o", output_exec], capture_output=True, text=True)
            if compile.returncode != 0:
                return jsonify({"output": compile.stderr})
            result = subprocess.run([output_exec], input=user_input, capture_output=True, text=True, timeout=5)

        elif language == "java":
            compile = subprocess.run(["javac", filepath], capture_output=True, text=True)
            if compile.returncode != 0:
                return jsonify({"output": compile.stderr})
            result = subprocess.run(["java", filename], input=user_input, capture_output=True, text=True, timeout=5)

        return jsonify({"output": result.stdout or result.stderr})

    except subprocess.TimeoutExpired:
        return jsonify({"output": "Execution timed out."})

    except Exception as e:
        return jsonify({"output": f"Error: {str(e)}"})

    finally:
        try:
            os.remove(filepath)
            if language in ["c", "cpp"]:
                os.remove(output_exec)
            elif language == "java":
                os.remove(f"{filename}.class")
        except:
            pass

if __name__ == "__main__":
    app.run(debug=True)
