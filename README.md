# EduPro Learner Intelligence

EduPro Learner Intelligence is a Streamlit-based learner analytics and personalized course recommendation system. It analyzes learner behavior, preferences, engagement, and performance to identify learner segments and provide personalized course recommendations.

## Project Overview

The system provides an interactive dashboard to analyze learner data and understand learning patterns across different learner segments.

### Project Statistics

- **3,000 Learners**
- **60 Courses**
- **10 Learner Segments**
- **15,000 Recommendations**

## Key Features

### 🏠 Overview
Provides an overall summary of the learning platform with important project statistics and key performance indicators.

### 👤 Learner Explorer
Allows users to select and explore individual learners, including:

- Learner segment
- Demographics
- Learning preferences
- Enrollment behavior
- Spending patterns
- Behavioral profile
- Personalized recommendations

### 🧩 Learner Segments
Provides insights into different learner segments through:

- Segment distribution
- Segment metrics
- Engagement analysis
- Segment-based recommendations

### 🤖 Personalized Recommendations
Provides ranked course recommendations for individual learners based on learner characteristics and recommendation scores.

Users can filter recommendations by:

- Learner
- Course level
- Course category
- Number of recommendations

### 📊 Analytics
Provides interactive learner analytics including:

- Gender distribution
- Preferred course level
- Preferred course category
- Age distribution
- Average spending
- Average course rating
- Average courses enrolled
- Segment-level spending analysis

## Technologies Used

- Python
- Pandas
- NumPy
- Altair
- Streamlit
- CSV
- GitHub

## Project Structure

```text
EduPro-Learner-Intelligence/
│
├── app.py
├── requirements.txt
├── README.md
│
└── data/
    ├── learner_profiles.csv
    ├── all_recommendations.csv
    ├── cluster_engagement.csv
    ├── segment_recommendations.csv
    └── top_recommended_courses.csv