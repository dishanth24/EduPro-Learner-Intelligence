import pandas as pd

file_path = "data/EduPro Online Platform (1).xlsx"

users = pd.read_excel(file_path, sheet_name="Users")
teachers = pd.read_excel(file_path, sheet_name="Teachers")
courses = pd.read_excel(file_path, sheet_name="Courses")
transactions = pd.read_excel(file_path, sheet_name="Transactions")

print("Users:", users.shape)
print("Teachers:", teachers.shape)
print("Courses:", courses.shape)
print("Transactions:", transactions.shape)

print("\n--- USERS ---")
print(users.head())

print("\n--- COURSES ---")
print(courses.head())

print("\n--- TRANSACTIONS ---")
print(transactions.head())

print("\nUsers columns:")
print(users.columns.tolist())

print("\nCourses columns:")
print(courses.columns.tolist())

print("\nTransactions columns:")
print(transactions.columns.tolist())

print("\n--- MISSING VALUES ---")

print("\nUsers:")
print(users.isnull().sum())

print("\nCourses:")
print(courses.isnull().sum())

print("\nTransactions:")
print(transactions.isnull().sum())
print("\n--- DUPLICATES ---")

print("Duplicate Users:", users.duplicated().sum())
print("Duplicate Courses:", courses.duplicated().sum())
print("Duplicate Transactions:", transactions.duplicated().sum())

print("\n--- DATA TYPES ---")

print("\nUsers:")
print(users.dtypes)

print("\nCourses:")
print(courses.dtypes)

print("\nTransactions:")
print(transactions.dtypes)

print("\n--- COURSE CATEGORIES ---")
print(courses["CourseCategory"].value_counts())

print("\n--- COURSE TYPES ---")
print(courses["CourseType"].value_counts())

print("\n--- COURSE LEVELS ---")
print(courses["CourseLevel"].value_counts())

print("\n--- USER DEMOGRAPHICS ---")

print("\nGender:")
print(users["Gender"].value_counts())

print("\nAge Statistics:")
print(users["Age"].describe())
print("\n--- TRANSACTION ANALYSIS ---")

print("\nTransaction Date Range:")
print("Start:", transactions["TransactionDate"].min())
print("End:", transactions["TransactionDate"].max())

print("\nAmount Statistics:")
print(transactions["Amount"].describe())

print("\n--- TRANSACTION ANALYSIS ---")

print("\nTransaction Date Range:")
print("Start:", transactions["TransactionDate"].min())
print("End:", transactions["TransactionDate"].max())

print("\nAmount Statistics:")
print(transactions["Amount"].describe())

# Merge transactions with course information

student_courses = transactions.merge(
    courses,
    on="CourseID",
    how="left"
)

print("\n--- MERGED STUDENT COURSE DATA ---")
print(student_courses.head())

print("\nShape:", student_courses.shape)

# Create learner profile base

learner_profiles = users[[
    "UserID",
    "Age",
    "Gender"
]].copy()

print("\n--- LEARNER PROFILE BASE ---")
print(learner_profiles.head())
print("\nNumber of learners:", len(learner_profiles))


# Engagement Feature: Total courses enrolled

course_counts = (
    student_courses.groupby("UserID")["CourseID"]
    .nunique()
    .reset_index(name="TotalCoursesEnrolled")
)

learner_profiles = learner_profiles.merge(
    course_counts,
    on="UserID",
    how="left"
)

learner_profiles["TotalCoursesEnrolled"] = (
    learner_profiles["TotalCoursesEnrolled"].fillna(0)
)

print("\n--- TOTAL COURSES ENROLLED ---")
print(learner_profiles[[
    "UserID",
    "TotalCoursesEnrolled"
]].head(10))

# Engagement Feature: Enrollment frequency

student_courses["TransactionMonth"] = (
    student_courses["TransactionDate"].dt.to_period("M")
)

enrollment_frequency = (
    student_courses.groupby("UserID")
    .agg(
        ActiveMonths=("TransactionMonth", "nunique"),
        TotalTransactions=("TransactionID", "count")
    )
    .reset_index()
)

enrollment_frequency["EnrollmentFrequency"] = (
    enrollment_frequency["TotalTransactions"]
    / enrollment_frequency["ActiveMonths"]
)

learner_profiles = learner_profiles.merge(
    enrollment_frequency[[
        "UserID",
        "EnrollmentFrequency"
    ]],
    on="UserID",
    how="left"
)

learner_profiles["EnrollmentFrequency"] = (
    learner_profiles["EnrollmentFrequency"].fillna(0)
)

print("\n--- ENROLLMENT FREQUENCY ---")
print(learner_profiles[[
    "UserID",
    "EnrollmentFrequency"
]].head(10))

# Behavioral Feature: Average spending

average_spending = (
    student_courses.groupby("UserID")["Amount"]
    .mean()
    .reset_index(name="AverageSpending")
)

learner_profiles = learner_profiles.merge(
    average_spending,
    on="UserID",
    how="left"
)

learner_profiles["AverageSpending"] = (
    learner_profiles["AverageSpending"].fillna(0)
)

print("\n--- AVERAGE SPENDING ---")
print(learner_profiles[[
    "UserID",
    "AverageSpending"
]].head(10))

# Preference Feature: Preferred course category

preferred_category = (
    student_courses.groupby("UserID")["CourseCategory"]
    .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else "Unknown")
    .reset_index(name="PreferredCategory")
)

learner_profiles = learner_profiles.merge(
    preferred_category,
    on="UserID",
    how="left"
)

learner_profiles["PreferredCategory"] = (
    learner_profiles["PreferredCategory"].fillna("Unknown")
)

print("\n--- PREFERRED CATEGORY ---")
print(learner_profiles[[
    "UserID",
    "PreferredCategory"
]].head(10))

# Preference Feature: Preferred course level

preferred_level = (
    student_courses.groupby("UserID")["CourseLevel"]
    .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else "Unknown")
    .reset_index(name="PreferredLevel")
)

learner_profiles = learner_profiles.merge(
    preferred_level,
    on="UserID",
    how="left"
)

learner_profiles["PreferredLevel"] = (
    learner_profiles["PreferredLevel"].fillna("Unknown")
)

print("\n--- PREFERRED LEVEL ---")
print(learner_profiles[[
    "UserID",
    "PreferredLevel"
]].head(10))

# Preference Feature: Average course rating

average_rating = (
    student_courses.groupby("UserID")["CourseRating"]
    .mean()
    .reset_index(name="AverageCourseRating")
)

learner_profiles = learner_profiles.merge(
    average_rating,
    on="UserID",
    how="left"
)

learner_profiles["AverageCourseRating"] = (
    learner_profiles["AverageCourseRating"].fillna(0)
)

print("\n--- AVERAGE COURSE RATING ---")
print(learner_profiles[[
    "UserID",
    "AverageCourseRating"
]].head(10))

# Behavioral Feature: Category diversity

category_diversity = (
    student_courses.groupby("UserID")["CourseCategory"]
    .nunique()
    .reset_index(name="CategoryDiversity")
)

learner_profiles = learner_profiles.merge(
    category_diversity,
    on="UserID",
    how="left"
)

learner_profiles["CategoryDiversity"] = (
    learner_profiles["CategoryDiversity"].fillna(0)
)

print("\n--- CATEGORY DIVERSITY ---")
print(learner_profiles[[
    "UserID",
    "CategoryDiversity"
]].head(10))

# Behavioral Feature: Learning depth index

level_scores = {
    "Beginner": 1,
    "Intermediate": 2,
    "Advanced": 3
}

student_courses["LevelScore"] = (
    student_courses["CourseLevel"].map(level_scores)
)

learning_depth = (
    student_courses.groupby("UserID")["LevelScore"]
    .mean()
    .reset_index(name="LearningDepthIndex")
)

learner_profiles = learner_profiles.merge(
    learning_depth,
    on="UserID",
    how="left"
)

learner_profiles["LearningDepthIndex"] = (
    learner_profiles["LearningDepthIndex"].fillna(0)
)

print("\n--- LEARNING DEPTH INDEX ---")
print(learner_profiles[[
    "UserID",
    "LearningDepthIndex"
]].head(10))

# Behavioral Feature: Total spending

total_spending = (
    student_courses.groupby("UserID")["Amount"]
    .sum()
    .reset_index(name="TotalSpending")
)

learner_profiles = learner_profiles.merge(
    total_spending,
    on="UserID",
    how="left"
)

learner_profiles["TotalSpending"] = (
    learner_profiles["TotalSpending"].fillna(0)
)

print("\n--- TOTAL SPENDING ---")
print(learner_profiles[[
    "UserID",
    "TotalSpending"
]].head(10))

print("\n--- LEARNER PROFILE ---")
print(learner_profiles.head())

print("\nShape:", learner_profiles.shape)

print("\nColumns:")
print(learner_profiles.columns.tolist())

print("\n--- NUMERICAL FEATURE STATISTICS ---")

numerical_features = [
    "Age",
    "TotalCoursesEnrolled",
    "EnrollmentFrequency",
    "AverageSpending",
    "AverageCourseRating",
    "CategoryDiversity",
    "LearningDepthIndex",
    "TotalSpending"
]

print(learner_profiles[numerical_features].describe())

# Prepare features for clustering

clustering_data = learner_profiles.drop(
    columns=["UserID"]
).copy()

# Convert categorical features into numerical values
clustering_data = pd.get_dummies(
    clustering_data,
    columns=["Gender", "PreferredCategory", "PreferredLevel"],
    drop_first=False
)

print("\n--- CLUSTERING DATA ---")
print("Shape:", clustering_data.shape)
print("\nColumns:")
print(clustering_data.columns.tolist())

from sklearn.preprocessing import StandardScaler

# Scale features for clustering

scaler = StandardScaler()

scaled_features = scaler.fit_transform(clustering_data)

print("\n--- SCALED FEATURES ---")
print("Shape:", scaled_features.shape)
print("Mean of first 5 features:", scaled_features.mean(axis=0)[:5])
print("Standard deviation of first 5 features:", scaled_features.std(axis=0)[:5])

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Elbow Method

inertia = []

for k in range(2, 11):
    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )
    kmeans.fit(scaled_features)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(range(2, 11), inertia, marker="o")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.title("Elbow Method for Optimal K")
plt.xticks(range(2, 11))
plt.grid(True)
plt.show()

from sklearn.metrics import silhouette_score

# Silhouette Score for different K values

silhouette_scores = []

for k in range(2, 11):
    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )
    
    labels = kmeans.fit_predict(scaled_features)
    
    score = silhouette_score(scaled_features, labels)
    silhouette_scores.append(score)

print("\n--- SILHOUETTE SCORES ---")

for k, score in zip(range(2, 11), silhouette_scores):
    print(f"K={k}: {score:.4f}")
    
# Final K-Means clustering

optimal_k = 10

kmeans = KMeans(
    n_clusters=optimal_k,
    random_state=42,
    n_init=10
)

learner_profiles["Cluster"] = kmeans.fit_predict(scaled_features)

print("\n--- CLUSTER ASSIGNMENTS ---")
print(learner_profiles[[
    "UserID",
    "Cluster"
]].head(10))

print("\nCluster Sizes:")
print(learner_profiles["Cluster"].value_counts().sort_index())

# Analyze learner segments

cluster_summary = learner_profiles.groupby("Cluster").agg({
    "Age": "mean",
    "TotalCoursesEnrolled": "mean",
    "EnrollmentFrequency": "mean",
    "AverageSpending": "mean",
    "AverageCourseRating": "mean",
    "CategoryDiversity": "mean",
    "LearningDepthIndex": "mean",
    "TotalSpending": "mean"
}).round(2)

print("\n--- CLUSTER PROFILE SUMMARY ---")
print(cluster_summary)
print("\n--- COMPLETE CLUSTER PROFILE ---")

pd.set_option("display.max_columns", None)

print(cluster_summary)


# Find the dominant preferences of each cluster

cluster_preferences = learner_profiles.groupby("Cluster").agg(
    PreferredCategory=("PreferredCategory",
                        lambda x: x.mode().iloc[0]),
    PreferredLevel=("PreferredLevel",
                    lambda x: x.mode().iloc[0])
).reset_index()

print("\n--- CLUSTER PREFERENCES ---")
print(cluster_preferences.to_string(index=False))

# Assign meaningful names to learner segments

segment_names = {
    0: "AI Beginner Learners",
    1: "Business Advanced Learners",
    2: "Cybersecurity Beginners",
    3: "Data Science Beginners",
    4: "Highly Engaged AI Explorers",
    5: "Digital Marketing Learners",
    6: "Advanced Machine Learning Learners",
    7: "Deep Design Learners",
    8: "Advanced Marketing Learners",
    9: "Advanced Web Development Learners"
}

learner_profiles["SegmentName"] = learner_profiles["Cluster"].map(
    segment_names
)

print("\n--- SEGMENT NAMES ---")
print(
    learner_profiles[
        ["UserID", "Cluster", "SegmentName"]
    ].head(20)
)

print("\nSegment Distribution:")
print(
    learner_profiles["SegmentName"]
    .value_counts()
)

# Save learner profiles

learner_profiles.to_csv(
    "learner_profiles.csv",
    index=False
)

print("\nLearner profiles saved successfully!")

# Prepare course recommendation data

recommendation_courses = courses[
    [
        "CourseID",
        "CourseName",
        "CourseCategory",
        "CourseType",
        "CourseLevel",
        "CoursePrice",
        "CourseDuration",
        "CourseRating"
    ]
].copy()

print("\n--- RECOMMENDATION COURSE DATA ---")
print(recommendation_courses.head(10))
print("\nNumber of courses:", len(recommendation_courses))
# Track courses already enrolled by each learner

enrolled_courses = (
    transactions.groupby("UserID")["CourseID"]
    .apply(set)
    .to_dict()
)

print("\n--- ENROLLED COURSES ---")

for user_id in list(enrolled_courses.keys())[:5]:
    print(user_id, enrolled_courses[user_id])
    
    
# Personalized course recommendation function

def recommend_courses(user_id, top_n=5):

    learner = learner_profiles[
        learner_profiles["UserID"] == user_id
    ].iloc[0]

    preferred_category = learner["PreferredCategory"]
    preferred_level = learner["PreferredLevel"]

    already_enrolled = enrolled_courses.get(user_id, set())

    candidates = recommendation_courses[
        ~recommendation_courses["CourseID"].isin(already_enrolled)
    ].copy()

    # Calculate recommendation score
    candidates["Score"] = 0.0

    candidates.loc[
        candidates["CourseCategory"] == preferred_category,
        "Score"
    ] += 4

    candidates.loc[
        candidates["CourseLevel"] == preferred_level,
        "Score"
    ] += 3

    candidates["Score"] += (
        candidates["CourseRating"] / 5
    ) * 2

    candidates.loc[
        candidates["CourseType"] == "Free",
        "Score"
    ] += 1

    # Sort by highest score
    recommendations = candidates.sort_values(
        "Score",
        ascending=False
    ).head(top_n)

    return recommendations[
        [
            "CourseID",
            "CourseName",
            "CourseCategory",
            "CourseType",
            "CourseLevel",
            "CourseRating",
            "Score"
        ]
    ]
    
# ============================================================
# STEP 38 - TEST THE RECOMMENDATION ENGINE
# ============================================================

test_user = "U00001"

print("\n" + "=" * 70)
print("RECOMMENDATIONS FOR", test_user)
print("=" * 70)

recommended = recommend_courses(
    test_user,
    top_n=5
)

print(recommended.to_string(index=False))


# ============================================================
# STEP 39 - TEST MULTIPLE LEARNERS
# ============================================================

test_users = [
    "U00001",
    "U00002",
    "U00003",
    "U00004",
    "U00005"
]

print("\n\n" + "=" * 70)
print("MULTIPLE LEARNER RECOMMENDATION TEST")
print("=" * 70)

for user_id in test_users:

    print("\n" + "-" * 70)
    print("LEARNER:", user_id)
    print("-" * 70)

    learner_info = learner_profiles[
        learner_profiles["UserID"] == user_id
    ].iloc[0]

    print(
        "Preferred Category:",
        learner_info["PreferredCategory"]
    )

    print(
        "Preferred Level:",
        learner_info["PreferredLevel"]
    )

    recommended = recommend_courses(
        user_id,
        top_n=5
    )

    print(recommended.to_string(index=False))


# ============================================================
# STEP 40 - GENERATE RECOMMENDATIONS FOR ALL LEARNERS
# ============================================================

all_recommendations = []

for user_id in learner_profiles["UserID"]:

    recommendations = recommend_courses(
        user_id,
        top_n=5
    )

    for rank, (_, course) in enumerate(
        recommendations.iterrows(),
        start=1
    ):

        all_recommendations.append({
            "UserID": user_id,
            "RecommendationRank": rank,
            "CourseID": course["CourseID"],
            "CourseName": course["CourseName"],
            "CourseCategory": course["CourseCategory"],
            "CourseType": course["CourseType"],
            "CourseLevel": course["CourseLevel"],
            "CourseRating": course["CourseRating"],
            "Score": course["Score"]
        })


all_recommendations = pd.DataFrame(
    all_recommendations
)

print("\n" + "=" * 70)
print("ALL LEARNER RECOMMENDATIONS")
print("=" * 70)

print(
    "Total recommendation records:",
    len(all_recommendations)
)

print(
    all_recommendations.head(20).to_string(index=False)
)


# ============================================================
# STEP 41 - CHECK RECOMMENDATION QUALITY
# ============================================================

print("\n" + "=" * 70)
print("RECOMMENDATION QUALITY CHECK")
print("=" * 70)

# Check for duplicate recommendations for the same learner
duplicate_recommendations = (
    all_recommendations
    .duplicated(
        subset=["UserID", "CourseID"]
    )
    .sum()
)

print(
    "Duplicate learner-course recommendations:",
    duplicate_recommendations
)


# Check that recommendations are not already enrolled
enrolled_lookup = (
    transactions
    .groupby("UserID")["CourseID"]
    .apply(set)
    .to_dict()
)

already_taken_count = 0

for _, row in all_recommendations.iterrows():

    user_id = row["UserID"]
    course_id = row["CourseID"]

    if course_id in enrolled_lookup.get(user_id, set()):
        already_taken_count += 1

print(
    "Already-enrolled courses recommended:",
    already_taken_count
)


# ============================================================
# STEP 42 - RECOMMENDATION PRECISION PROXY
# ============================================================

print("\n" + "=" * 70)
print("RECOMMENDATION PRECISION PROXY")
print("=" * 70)

# A recommendation is considered category-relevant
# when it matches the learner's preferred category.

recommendation_with_profiles = all_recommendations.merge(
    learner_profiles[
        [
            "UserID",
            "PreferredCategory",
            "PreferredLevel",
            "SegmentName"
        ]
    ],
    on="UserID",
    how="left"
)

category_matches = (
    recommendation_with_profiles["CourseCategory"]
    ==
    recommendation_with_profiles["PreferredCategory"]
)

level_matches = (
    recommendation_with_profiles["CourseLevel"]
    ==
    recommendation_with_profiles["PreferredLevel"]
)

category_precision = category_matches.mean()

level_precision = level_matches.mean()

print(
    f"Category Relevance Precision: "
    f"{category_precision:.4f}"
)

print(
    f"Level Relevance Precision: "
    f"{level_precision:.4f}"
)


# ============================================================
# STEP 43 - SEGMENT-WISE RECOMMENDATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("SEGMENT-WISE RECOMMENDATION ANALYSIS")
print("=" * 70)

segment_recommendations = (
    recommendation_with_profiles
    .groupby(
        [
            "SegmentName",
            "CourseCategory"
        ]
    )
    .size()
    .reset_index(
        name="RecommendationCount"
    )
)

segment_recommendations = (
    segment_recommendations
    .sort_values(
        [
            "SegmentName",
            "RecommendationCount"
        ],
        ascending=[True, False]
    )
)

print(
    segment_recommendations
    .to_string(index=False)
)


# ============================================================
# STEP 44 - TOP RECOMMENDED COURSES
# ============================================================

print("\n" + "=" * 70)
print("TOP RECOMMENDED COURSES")
print("=" * 70)

top_recommended_courses = (
    all_recommendations
    .groupby(
        [
            "CourseID",
            "CourseName",
            "CourseCategory"
        ]
    )
    .size()
    .reset_index(
        name="RecommendationCount"
    )
    .sort_values(
        "RecommendationCount",
        ascending=False
    )
)

print(
    top_recommended_courses
    .head(10)
    .to_string(index=False)
)


# ============================================================
# STEP 45 - CLUSTER ENGAGEMENT ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("CLUSTER ENGAGEMENT ANALYSIS")
print("=" * 70)

cluster_engagement = (
    learner_profiles
    .groupby("SegmentName")
    .agg(
        Learners=("UserID", "count"),
        AvgCourses=("TotalCoursesEnrolled", "mean"),
        AvgEnrollmentFrequency=("EnrollmentFrequency", "mean"),
        AvgSpending=("AverageSpending", "mean"),
        AvgCourseRating=("AverageCourseRating", "mean"),
        AvgCategoryDiversity=("CategoryDiversity", "mean"),
        AvgLearningDepth=("LearningDepthIndex", "mean"),
        TotalSpending=("TotalSpending", "sum")
    )
    .reset_index()
)

print(
    cluster_engagement
    .to_string(index=False)
)


# ============================================================
# STEP 46 - SAVE FINAL LEARNER PROFILES
# ============================================================

learner_profiles.to_csv(
    "learner_profiles.csv",
    index=False
)

print("\nLearner profiles saved successfully!")


# ============================================================
# STEP 47 - SAVE ALL RECOMMENDATIONS
# ============================================================

all_recommendations.to_csv(
    "all_recommendations.csv",
    index=False
)

print("All recommendations saved successfully!")


# ============================================================
# STEP 48 - SAVE SEGMENT ANALYSIS
# ============================================================

cluster_engagement.to_csv(
    "cluster_engagement.csv",
    index=False
)

segment_recommendations.to_csv(
    "segment_recommendations.csv",
    index=False
)

top_recommended_courses.to_csv(
    "top_recommended_courses.csv",
    index=False
)

print("Segment analysis files saved successfully!")


# ============================================================
# STEP 49 - FINAL PROJECT SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("EDUPRO STUDENT SEGMENTATION & RECOMMENDATION SYSTEM")
print("=" * 70)

print("\nDATASET")
print("Learners:", len(users))
print("Teachers:", len(teachers))
print("Courses:", len(courses))
print("Transactions:", len(transactions))

print("\nSEGMENTATION")
print("Number of clusters:", learner_profiles["Cluster"].nunique())
print(
    "Number of learner segments:",
    learner_profiles["SegmentName"].nunique()
)

print("\nRECOMMENDATION SYSTEM")
print(
    "Recommendations per learner:",
    all_recommendations["RecommendationRank"].max()
)

print(
    "Total recommendations generated:",
    len(all_recommendations)
)

print(
    "Category relevance precision:",
    f"{category_precision:.4f}"
)

print(
    "Level relevance precision:",
    f"{level_precision:.4f}"
)

print(
    "Already-enrolled recommendations:",
    already_taken_count
)

print("\nOUTPUT FILES")
print("1. learner_profiles.csv")
print("2. all_recommendations.csv")
print("3. cluster_engagement.csv")
print("4. segment_recommendations.csv")
print("5. top_recommended_courses.csv")

print("\n" + "=" * 70)
print("PROJECT DATA SCIENCE PIPELINE COMPLETED!")
print("=" * 70)