import datetime
import os
import pandas as pd
import streamlit as st

from correlation import Analysis
from main import Simulation
from metrics import run_metrics

rooms_and_objects = {
    "Classroom": ["Desk", "Book", "Computer"],
    "Auditorium": ["Chair1", "Screen", "Hand"],
    "Café": ["Chair2", "Student", "Table"],
}

directory_path = "../data"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)


def main():
    st.set_page_config(page_title="IVLE-Sim",
                       page_icon=":material/robot_2:",
                       initial_sidebar_state="expanded",
                       menu_items={
                           "Get Help": "https://github.com/diascarolina",
                           "Report a bug": "https://github.com/diascarolina",
                           "About": "IVLE-Sim: Immersive Virtual Learning Environment Simulation"
                       })
    st.title("IVLE-Sim: Immersive Virtual Learning Environment Simulation")
    "---"

    st.sidebar.title("IVLE-Sim")
    st.sidebar.header("Simulation Parameters")

    st.sidebar.write(
        "Please select the number of students, the duration of the simulation and the start date."
    )

    num_users = st.sidebar.number_input(label="Number of Students",
                                        min_value=1,
                                        value=100,
                                        step=10)

    duration = st.sidebar.number_input(label="Duration of Simulation (days)",
                                       min_value=1,
                                       value=200,
                                       step=10)

    start_date = st.sidebar.date_input("Start Date", datetime.date(2024, 1, 1))

    """This is a simulation of student interactions in a virtual environment.
    The simulation generates a CSV file with the interactions of each student. 
    You can then calculate metrics based on this data and display charts based on the metrics."""

    "The simulation has the following rooms and objects:"
    st.table(rooms_and_objects)

    st.info("Change the parameters on the sidebar and click the following button to run the "
            "script.")

    df_name = f"simulation_data_{num_users}u_{duration}d"
    df_path = f"{directory_path}/{df_name}.csv"
    df_path_metrics = f"../data/metrics_{df_name}.csv"

    if st.button(":arrow_forward: Run Simulation, Metrics and Analysis", type="primary"):
        with st.spinner('Running Simulation and Results...'):
            st.header("#")
            st.header("Simulation Results")
            sim = Simulation(num_users=num_users,
                             rooms_and_objects=rooms_and_objects,
                             duration=duration,
                             start_date=start_date.strftime("%Y-%m-%d"),
                             generate_csv_file=True,
                             df_path=df_path)
            sim.run_simulation()
            df = pd.read_csv(df_path)
            st.dataframe(df)
            st.success("Simulation completed and CSV file generated!", icon="✅")

            st.header("#")
            st.header("Calculated Metrics")
            metrics = run_metrics(simulation_df_name=df_name,
                                  rooms_and_objects=rooms_and_objects,
                                  weights=None)

            st.dataframe(metrics)
            st.success("Metrics calculated and CSV file generated!!", icon="✅")

            st.header("#")
            st.header("Correlation Analysis")
            analysis = Analysis(df_path_metrics)
            analysis_dict = analysis.anova()
            col1, col2 = st.columns(2)
            col1.metric("F-Value",
                        analysis_dict['F-value'],
                        help="The bigger the F-Value, the more significant the correlation.")
            col2.metric("P-Value",
                        analysis_dict['P-value'],
                        help="The smaller the P-Value, the more significant the correlation.")
            st.success("Correlation analysis completed!", icon="✅")

            st.header("#")
            st.header("Engagement Scores by Engagement Levels")
            fig = analysis.plot_kde(st=True)
            st.pyplot(fig)
            st.success("Plot generated!", icon="✅")

    st.sidebar.write("---")
    st.sidebar.text("Created by Carolina Dias, 2024")
    st.sidebar.markdown(
        """<a href="https://github.com/diascarolina/student-interaction-data-generation">
        <img src="https://img.shields.io/badge/GitHub-100000?style=flat-square&logo=github&logoColor=white">
        </a>""",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
