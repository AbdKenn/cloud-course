import os
import predict
import streamlit as st
from loguru import logger

rootDir = os.path.dirname(__file__)


@st.cache(suppress_st_warning=True)
def get_fvalue(val):
    feature_dict = {"No": 1, "Yes": 2}
    for key, value in feature_dict.items():
        if val == key:
            return value


def get_value(val, my_dict):
    for key, value in my_dict.items():
        if val == key:
            return value


dict_civility = {
    "Homme": "1",
    "Femme": "2",
    "Autre": "3"
}

app_mode = st.sidebar.selectbox('Select Page', ['Home', 'Prediction'])
# app_mode = "Prediction"
if app_mode == 'Home':

    st.title("Price prediction web app")
    st.header("this is the price prediction service web app demonstration")
    st.write("Please fill in all the forms to get your MER price")
    st.image("ci.jpg")
    # st.write("used model (XGBoost Regressor) expression : ")
    # st.latex(r''' 1/1+exp(-x) ''')
    st.image("logo.jpg")

elif app_mode == 'Prediction':

    st.subheader("Please fill in all the forms to get your predicted price")
    st.sidebar.header("Informations about the client :")

    Id = "TEST-ID"
    nb_persons_to_insure = st.sidebar.radio('Personnes à assurer', options=[1, 2, 3, 4, 5])
    already_have_health_insurance = st.sidebar.radio('Vous avez déjà une complémentaire de santé ?', ("0", "1"))
    civility = st.sidebar.radio('Sexe', options=["Homme", "Femme", "Autre"])
    civility = dict_civility[civility]
    birth_date = st.sidebar.text_input("Date de naissance (format : 'dd/mm/YYYY')", value="")
    social_regime = st.sidebar.radio('Régime social', options=['3', '4', '5', '6', '7'])
    start_date = st.sidebar.text_input("Date de début de contrat (format : 'dd/mm/YYYY')", value="")
    nb_children_to_insure = st.sidebar.radio('Personnes à assurer', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    demand_g = st.sidebar.radio('Niveau de garantie sur les soins généraux souhaité', options=['0', '1', '2', '3', '4', '5'])
    demand_h = st.sidebar.radio('Niveau de garantie sur les soins hospitaliers souhaité', options=['0', '1', '2', '3', '4', '5'])
    demand_o = st.sidebar.radio('Niveau de garantie sur les soins optiques souhaité', options=['0', '1', '2', '3', '4', '5'])
    demand_d = st.sidebar.radio('Niveau de garantie sur les soins dentaires souhaité', options=['0', '1', '2', '3', '4', '5'])
    offer_g = st.sidebar.radio('Niveau de garantie sur les soins généraux offert', options=['0', '1', '2', '3', '4', '5'])
    offer_h = st.sidebar.radio('Niveau de garantie sur les soins hospitaliers offert', options=['0', '1', '2', '3', '4', '5'])
    offer_o = st.sidebar.radio('Niveau de garantie sur les soins optiques offert', options=['0', '1', '2', '3', '4', '5'])
    offer_d = st.sidebar.radio('Niveau de garantie sur les soins dentaires offert', options=['0', '1', '2', '3', '4', '5'])

    json_content = [{
        "usheet_id": Id,
        "tarification_id": Id,
        "product_id": Id,
        "nb_person_to_ensure": nb_persons_to_insure,
         "already_have_health_insurance": already_have_health_insurance,
         "Civility": civility,
         "BirthDate": birth_date,
         "social_regime": social_regime,
         "QS1_11": start_date,
         "child_number": nb_children_to_insure,
         "demand_G": demand_g,
         "demand_H": demand_h,
         "demand_O": demand_o,
         "demand_D": demand_d,
         "offer_D": offer_d,
         "offer_G": offer_g,
         "offer_H": offer_h,
         "offer_O": offer_o
    }]
    logger.info(json_content)

    if st.button("Predict"):
        predicted_dict, x = predict.predict(predict.model, json_content, predict.out_data, predict.entite)
        st.write("Predicted price summary in € : ", predicted_dict)
