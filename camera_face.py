import cv2
import mediapipe as mp
import os
import shutil

def calculate_alignment_score(landmarks):
    nose_tip = landmarks.landmark[1]  # Nose tip
    chin = landmarks.landmark[152]  # Chin
    left_eye_inner = landmarks.landmark[133]  # Left eye inner corner
    right_eye_inner = landmarks.landmark[362]  # Right eye inner corner

    eye_center_x = (left_eye_inner.x + right_eye_inner.x) / 2
    horizontal_alignment = abs(eye_center_x - nose_tip.x)
    vertical_alignment = abs(nose_tip.x - chin.x)

    score = max(0, 1 - (horizontal_alignment + vertical_alignment))
    return score

def process_image(image_path):
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)

    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image {image_path}")
        return None

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]
        return calculate_alignment_score(face_landmarks)
    
    return 0

def rank_images(directory):
    image_scores = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(root, file_name)
                score = process_image(file_path)
                if score is not None:
                    image_scores.append((file_path, score))
    
    ranked_images = sorted(image_scores, key=lambda x: x[1], reverse=True)
    return ranked_images

if __name__ == "__main__":
    print("Image Ranking Based on Frontal Pose")
    input_dir = input("Enter the directory containing images: ")
    output_dir = os.path.join(input_dir, "ranking")
    os.makedirs(output_dir, exist_ok=True)

    ranked_images = rank_images(input_dir)
    
    print("\nSaving Ranked Images:")
    for rank, (file_path, score) in enumerate(ranked_images, start=1):
        new_file_name = f"{rank:04d}.jpg"
        new_file_path = os.path.join(output_dir, new_file_name)
        shutil.copy(file_path, new_file_path)
        print(f"{new_file_name} - Score: {score:.2f}")
    
    print(f"\nAll ranked images saved in: {output_dir}")
    
    limit = int(input("Enter the number of top images to save: "))
    ranking_limit_dir = os.path.join(input_dir, "ranking_limit")
    os.makedirs(ranking_limit_dir, exist_ok=True)
    
    for rank, (file_path, score) in enumerate(ranked_images[:limit], start=1):
        new_file_name = f"{rank:04d}.jpg"
        new_file_path = os.path.join(ranking_limit_dir, new_file_name)
        shutil.copy(file_path, new_file_path)
        print(f"{new_file_name} saved in ranking_limit")
    
    print(f"\nTop {limit} images saved in: {ranking_limit_dir}")