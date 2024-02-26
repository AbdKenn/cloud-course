import os
import pandas as pd
import pickle
import json
import numpy as np
from datetime import datetime
import xgboost
import sklearn
from google.cloud import bigquery

from loguru import logger
import time


def mapFromjSON(json_content):
    if isinstance(json_content, list):
        df = pd.DataFrame.from_records(json_content)
    else:
        content = json_content.copy()
        for k, v in content.items():
            content[k] = [v]
        df = pd.DataFrame(content)
    return df



def calculate_age(birthdate):
    today = datetime.today()
    birthdate = datetime.strptime(birthdate, '%d/%m/%Y')
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def calculate_date_difference(date1, date2):
    date1 = datetime.strptime(date1, '%d/%m/%Y')
    # date2 = datetime.strptime(date2, '%d/%m/%Y')
    difference = abs((date2 - date1).days)
    return difference


def load_data_to_gbq(df, create=False):
    project_id = "mass-price-regression"
    dataset_ref = "mass_price_regression"
    table_name = "mass_price_regression"
    table_id = f"{project_id}.{dataset_ref}.{table_name}"

    client = bigquery.Client(project=project_id)
    # table = client.get_table(table_id)

    if create:
        try:
            table = bigquery.Table(table_id)
            table = client.create_table(table, exists_ok=False)
        except Exception as e:
            logger.info("Table : " + table_id + " already exist")

    job = client.load_table_from_dataframe(
        df, table_id
    ).result()


def quantitative_variables_preparation(df, out_data, entite):
    df_quanti = df.copy()
    with open(out_data + entite + "_imput_quanti.json",
              encoding="utf-8") as f:
        imput_quanti = json.load(f)

    quanti_vars = [c for c in imput_quanti]

    for col in df_quanti.columns:
        df_quanti[col] = np.where(
            df_quanti[col] == "", np.nan, df_quanti[col]
        )
        if col not in imput_quanti:
            # logger.info(col + " not in imput quanti JSON file")
            df_quanti.drop(col, axis=1, inplace=True)
        else:
            df_quanti[col].fillna(imput_quanti[col], inplace=True)

    reducer = pickle.load(
        open(
            out_data + "descritizers/" + entite +
            "_quanti_descritizer_" + "StandardScaler", 'rb'
        ))
    # logger.info("Reducer model for " + col + " loaded successfully!")

    if reducer:
        df_quanti[quanti_vars] = reducer.transform(np.array(df_quanti[quanti_vars]))

    return df_quanti


def qualitative_variables_preparation(df, out_data, entite):
    df_quali = df.copy()
    with open(out_data + entite + "_qualitative_groups.json",
              encoding="utf-8") as f:
        quali_json_all = json.load(f)

    quali_vars = [c for c in quali_json_all]

    for col in df_quali.columns:
        if col in quali_json_all:
            df_quali[col] = np.where(
                df_quali[col] == "", np.nan, df_quali[col]
            )
            df_quali[col].fillna("Manquant", inplace=True)
            variable_groups = quali_json_all[col]

            for v in list(df_quali[col].unique()):
                if v not in list(variable_groups):
                    logger.info("Value " + str(v) + " not in model trained values for " + str(col))
                    logger.info("This value will be used as a missing one")
                    df_quali[col] = np.where(
                        df_quali[col] == v, "Manquant", df_quali[col]
                    )

        else:
            df_quali.drop(col, axis=1, inplace=True)
            # logger.info(col + " dropped (not in json groups file)!")

    df_quali = pd.get_dummies(df_quali)

    return df_quali


def get_dummies_keep_reference_variables(df, entite):

    df_c = pd.get_dummies(df)

    with open(out_data + entite + "_variable_reference.json", encoding="utf-8") as f:
        var_reference = json.load(f)

    with open(out_data + entite + "_used_vars.json", encoding="utf-8") as f:
        used_vars = json.load(f)
    used_vars = used_vars[entite]

    col_ref_list = var_reference[entite] +\
        [col for col in df_c.columns if col.endswith("_99")]
    df_c = df_c[[col for col in df_c.columns if col not in col_ref_list]]

    for idx, c in enumerate(used_vars):
        if c != "Intercept":
            if c not in df_c.columns:
                df_c[c] = 0
    df_c = df_c[[c for c in used_vars if c != "Intercept"]]

    return df_c


def predict(model, x, out_data, entite):
    logger.info(x)
    x = mapFromjSON(x)
    try:
        x["Age"] = x["BirthDate"].map(calculate_age)
        x["insurance_start"] = x["QS1_11"].apply(lambda s: calculate_date_difference(s, datetime.today()))

        df_quanti = quantitative_variables_preparation(x, out_data, entite)
        df_quali = qualitative_variables_preparation(x, out_data, entite)
        X_to_pred = pd.concat([df_quanti, df_quali], axis=1)
        X_to_pred = get_dummies_keep_reference_variables(X_to_pred, entite)
        predicted = list(model.predict(X_to_pred))
        x["predicted_price"] = predicted
        predicted_dict = {"min": min(predicted) - 9, "mean": np.mean(predicted) + 0, "max": max(predicted) + 9}
        x["predicted_dict"] = str(predicted_dict)
        # try:
        #     logger.info("Writing to GBQ ...")
        #     load_data_to_gbq(x, create=False)
        # except Exception as e:
        #     logger.warning("Writing to BGQ failed : " + str(e))
        #     logger.info(x.to_dict("records"))
    except Exception as e:
        logger.warning("An error has occured ... ")
        logger.error(e)
        predicted = [np.nan]
        x["predicted_price"] = predicted
        predicted_dict = dict()

    logger.info(predicted_dict)

    return predicted_dict, x


business_name = "health_price_regression"
prefix_out = ""
entite = "mass"
rootDir = os.path.dirname(os.path.abspath(__file__))
out_data = rootDir + "/"
model_name = "XGBoost"
model = pickle.load(open(out_data + model_name +
                        "_score_" + business_name + "_" + prefix_out + "_" +
                        entite + ".pickle",
                        'rb'))
