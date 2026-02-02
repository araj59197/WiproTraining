from flask import Flask, jsonify, request, render_template_string
from datetime import datetime

app = Flask(__name__)

# In-memory patient database
patients = [
    {
        "id": 1,
        "name": "John Doe",
        "age": 45,
        "gender": "Male",
        "contact": "9876543210",
        "disease": "Diabetes",
        "doctor": "Dr. Smith",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "age": 32,
        "gender": "Female",
        "contact": "9876543211",
        "disease": "Hypertension",
        "doctor": "Dr. Johnson",
    },
]


def find_patient(patient_id):
    return next((p for p in patients if p["id"] == patient_id), None)


# API Endpoints
@app.route("/api/patients", methods=["GET"])
def get_patients():
    return jsonify(patients), 200


@app.route("/api/patients", methods=["POST"])
def add_patient():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    new_id = patients[-1]["id"] + 1 if patients else 1
    new_patient = {
        "id": new_id,
        "name": data.get("name"),
        "age": data.get("age"),
        "gender": data.get("gender"),
        "contact": data.get("contact"),
        "disease": data.get("disease"),
        "doctor": data.get("doctor"),
    }
    patients.append(new_patient)
    return jsonify(new_patient), 201


@app.route("/api/patients/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    patient = find_patient(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify(patient), 200


@app.route("/api/patients/<int:patient_id>", methods=["PUT"])
def update_patient(patient_id):
    patient = find_patient(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    data = request.get_json()
    patient["name"] = data.get("name", patient["name"])
    patient["age"] = data.get("age", patient["age"])
    patient["gender"] = data.get("gender", patient["gender"])
    patient["contact"] = data.get("contact", patient["contact"])
    patient["disease"] = data.get("disease", patient["disease"])
    patient["doctor"] = data.get("doctor", patient["doctor"])

    return jsonify(patient), 200


# Web Pages
@app.route("/")
def home():
    return render_template_string(REGISTRATION_FORM)


@app.route("/patients")
def patients_list():
    return render_template_string(PATIENTS_LIST, patients=patients)


@app.route("/register", methods=["POST"])
def register_patient():
    name = request.form.get("name")
    age = request.form.get("age")
    gender = request.form.get("gender")
    contact = request.form.get("contact")
    disease = request.form.get("disease")
    doctor = request.form.get("doctor")

    new_id = patients[-1]["id"] + 1 if patients else 1
    new_patient = {
        "id": new_id,
        "name": name,
        "age": int(age) if age else None,
        "gender": gender,
        "contact": contact,
        "disease": disease,
        "doctor": doctor,
    }
    patients.append(new_patient)

    return render_template_string(SUCCESS_PAGE, patient=new_patient)


# HTML Templates
REGISTRATION_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Patient Registration - Hospital Management</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 600px;
            width: 100%;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        
        .header i {
            font-size: 50px;
            margin-bottom: 15px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .header h1 {
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .form-content {
            padding: 40px 30px;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        .form-group.full-width {
            grid-column: 1 / -1;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #333;
            font-size: 14px;
        }
        
        label i {
            margin-right: 8px;
            color: #667eea;
        }
        
        input[type="text"],
        input[type="number"],
        input[type="tel"],
        select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s ease;
        }
        
        input[type="text"]:focus,
        input[type="number"]:focus,
        input[type="tel"]:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .gender-group {
            display: flex;
            gap: 20px;
            margin-top: 8px;
        }
        
        .radio-option {
            flex: 1;
            position: relative;
        }
        
        .radio-option input[type="radio"] {
            position: absolute;
            opacity: 0;
        }
        
        .radio-option label {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 400;
        }
        
        .radio-option input[type="radio"]:checked + label {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-color: #667eea;
            color: white;
        }
        
        .radio-option label i {
            margin-right: 8px;
            font-size: 18px;
        }
        
        select {
            cursor: pointer;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23667eea' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 15px center;
        }
        
        .submit-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
            font-family: 'Poppins', sans-serif;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        
        .submit-btn i {
            margin-right: 10px;
        }
        
        .links {
            text-align: center;
            margin-top: 25px;
            padding-top: 25px;
            border-top: 2px solid #f0f0f0;
        }
        
        .links a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .links a:hover {
            color: #764ba2;
        }
        
        .links a i {
            margin-right: 8px;
        }
        
        @media (max-width: 768px) {
            .form-row {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <i class="fas fa-hospital"></i>
            <h1>Patient Registration</h1>
            <p>Complete the form below to register a new patient</p>
        </div>
        
        <div class="form-content">
            <form id="patientForm" action="/register" method="POST">
                <div class="form-row">
                    <div class="form-group">
                        <label for="name"><i class="fas fa-user"></i>Patient Name</label>
                        <input type="text" id="name" name="name" placeholder="Enter full name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="age"><i class="fas fa-birthday-cake"></i>Age</label>
                        <input type="number" id="age" name="age" placeholder="Enter age" min="0" max="150" required>
                    </div>
                </div>
                
                <div class="form-group">
                    <label><i class="fas fa-venus-mars"></i>Gender</label>
                    <div class="gender-group">
                        <div class="radio-option">
                            <input type="radio" id="male" name="gender" value="Male" required>
                            <label for="male"><i class="fas fa-mars"></i>Male</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" id="female" name="gender" value="Female">
                            <label for="female"><i class="fas fa-venus"></i>Female</label>
                        </div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="contact"><i class="fas fa-phone"></i>Contact Number</label>
                    <input type="tel" id="contact" name="contact" placeholder="Enter 10-digit number" pattern="[0-9]{10}" required>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="disease"><i class="fas fa-stethoscope"></i>Disease</label>
                        <input type="text" id="disease" name="disease" placeholder="Enter diagnosis" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="doctor"><i class="fas fa-user-md"></i>Doctor Assigned</label>
                        <select id="doctor" name="doctor" required>
                            <option value="">Select Doctor</option>
                            <option value="Dr. Smith">Dr. Smith</option>
                            <option value="Dr. Johnson">Dr. Johnson</option>
                            <option value="Dr. Williams">Dr. Williams</option>
                            <option value="Dr. Brown">Dr. Brown</option>
                        </select>
                    </div>
                </div>
                
                <button type="submit" class="submit-btn">
                    <i class="fas fa-check-circle"></i>Register Patient
                </button>
                
                <div class="links">
                    <a href="/patients"><i class="fas fa-list"></i>View All Patients</a>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
"""

PATIENTS_LIST = """
<!DOCTYPE html>
<html>
<head>
    <title>Patients List</title>
    <style>
        body { font-family: Arial; margin: 50px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        h2 { color: #333; }
    </style>
</head>
<body>
    <h2>Registered Patients</h2>
    <table id="patientsTable">
        <thead>
            <tr>
                <th>ID</th>
                <th class="patient-name">Name</th>
                <th class="patient-age">Age</th>
                <th>Gender</th>
                <th>Contact</th>
                <th class="patient-disease">Disease</th>
                <th class="patient-doctor">Doctor</th>
            </tr>
        </thead>
        <tbody>
            {% for patient in patients %}
            <tr class="patient-row">
                <td>{{ patient.id }}</td>
                <td class="patient-name">{{ patient.name }}</td>
                <td class="patient-age">{{ patient.age }}</td>
                <td>{{ patient.gender }}</td>
                <td>{{ patient.contact }}</td>
                <td class="patient-disease">{{ patient.disease }}</td>
                <td class="patient-doctor">{{ patient.doctor }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <br>
    <a href="/">Register New Patient</a>
</body>
</html>
"""

SUCCESS_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Registration Successful</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        .success { background-color: #d4edda; border: 1px solid #c3e6cb; padding: 20px; border-radius: 5px; }
        h2 { color: #155724; }
    </style>
</head>
<body>
    <div class="success">
        <h2>Patient Registered Successfully!</h2>
        <p><strong>Name:</strong> {{ patient.name }}</p>
        <p><strong>Age:</strong> {{ patient.age }}</p>
        <p><strong>Disease:</strong> {{ patient.disease }}</p>
        <p><strong>Doctor:</strong> {{ patient.doctor }}</p>
    </div>
    <br>
    <a href="/">Register Another Patient</a> | 
    <a href="/patients">View All Patients</a>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True, port=5002)
