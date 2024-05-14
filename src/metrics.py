import pandas as pd


class Metrics:
    def __init__(self,
                 data: pd.DataFrame,
                 weights: dict[str, float] = None,
                 total_objects: list[str] = None):
        self.data = data
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data['duration'] = pd.to_timedelta(self.data['duration'])
        if weights is None:
            weights = {'time': 0.25, 'frequency': 0.25, 'diversity': 0.25, 'depth': 0.25}
        self.weights = weights
        self.total_objects = total_objects

    def calculate_per_user(self):
        user_metrics = []
        for username, group in self.data.groupby('username'):
            user_metrics.append({
                "username": username,
                "Total Interaction Time": self.total_interaction_time(group),
                "Interaction Frequency": self.interaction_frequency(group),
                "Interaction Diversity": self.interaction_diversity(group),
                "Interaction Depth": self.interaction_depth(group),
                "Engagement Score": self.engagement_score(group),
                "Engagement Level": group['engagement_level'].iloc[0]
            })
        return pd.DataFrame(user_metrics)

    @staticmethod
    def total_interaction_time(user_data):
        return user_data['duration'].sum().total_seconds()

    @staticmethod
    def interaction_frequency(user_data):
        return user_data[user_data['activity_type'] == 'interaction'].shape[0]

    def interaction_diversity(self, user_data):
        unique_interactions = user_data[user_data['activity_type'] == 'interaction'][
            'object'].nunique()
        total_possible_interactions = len(self.total_objects)
        return unique_interactions / total_possible_interactions if total_possible_interactions > 0 else 0

    def interaction_depth(self, user_data):
        frequency = self.interaction_frequency(user_data)
        if frequency == 0:
            return 0
        return self.total_interaction_time(user_data) / frequency

    def engagement_score(self, user_data):
        score = (self.weights['time'] * self.total_interaction_time(user_data) +
                 self.weights['frequency'] * self.interaction_frequency(user_data) +
                 self.weights['diversity'] * self.interaction_diversity(user_data) +
                 self.weights['depth'] * self.interaction_depth(user_data))
        return score

    @staticmethod
    def normalise(dataframe):
        for column in dataframe.columns[1:-1]:  # Skip the 'username' column
            min_val = dataframe[column].min()
            max_val = dataframe[column].max()
            dataframe[column] = (dataframe[column] - min_val) / (
                        max_val - min_val) if max_val > min_val else dataframe[column]
        return dataframe


if __name__ == "__main__":
    interaction_data = pd.read_csv('../data/interaction_data.csv')

    rooms_and_objects_dict = {
        "Classroom": ["Desk", "Chair1", "Book", "Computer"],
        "Auditorium": ["Chair2", "Screen", "Hand"],
        "Café": ["Chair3", "Student", "Table"],
    }
    objects = [obj_name for sublist in rooms_and_objects_dict.values() for obj_name in sublist]

    metric_weights = {'time': 0.25, 'frequency': 0.25, 'diversity': 0.25, 'depth': 0.25}

    metrics = Metrics(data=interaction_data, weights=metric_weights, total_objects=objects)

    results_df = metrics.calculate_per_user()
    normalised_results = metrics.normalise(results_df)

    normalised_results.to_csv('../data/normalised_results.csv', index=False)

    print(normalised_results)
