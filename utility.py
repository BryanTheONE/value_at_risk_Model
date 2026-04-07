# %%
# Preparazione ambiente 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.api as sm
from scipy.stats import ttest_ind
import yfinance as yf
import pickle
from scipy.stats import chi2

# %%
def get_historical_data(ticker_list: list, period="5y", interval="1d"):
    """
    Scarica i prezzi di chiusura per una lista di ticker.
        
        ticker_list: Lista dei simboli da yfinance
        period: periodo serie
        interval: frequenza dati
        
    ourput:pd.DataFrame: Prezzi di chiusura Adjusted
    """
    # in caso di errore (yf.download()["Adj Close"]) Adj non Defined provare auto_adjust = False 
    data = yf.download(ticker_list, period=period, interval=interval, auto_adjust= True)["Close"]
    return data

# %%
def calculate_log_returns(df_prices):
    """
    Calcola i log-returns e dataclean NaN
    """    
    log_returns = np.log(df_prices / df_prices.shift(1)).dropna()
    return log_returns

def save_to_pickle(df_log_returns, file_name: str):
    """salca df in formato pickle"""
    with open(f"{file_name}.pkl", "wb") as f:
        pickle.dump(obj, f)

def load_from_pickle(file_name):
    """Carica un oggetto da un file pickle."""
    with open(f"{file_name}.pkl", "rb") as f:
        return pickle.load(f)

# %%
def data_slicer(df_returns, event_date: str, pre_event_days=600, gap_days=15, post_event_days=250):
    """
    Divide i rendimenti in due periodi: Normalità (Pre-evento) e Distress (Post-evento).
    
    Args:
        df_returns: dataFrame con log-returns
        event_date: data slicer
        pre_event_days: lunghezza della finestra di stima,
        gap_days: giorni di 'cuscinetto' prima dell'evento,
        post_event_days: lunghezza della finestra di impatto,
    """
    # Gestione data e timezone
    t_event = pd.to_datetime(event_date)
    if df_returns.index.tz is not None:
        t_event = t_event.tz_localize(df_returns.index.tz)

    # crezione 2 df uno per ogni scenario
    start_normal = t_event - pd.offsets.BusinessDay(n=pre_event_days)
    end_normal   = t_event - pd.offsets.BusinessDay(n=gap_days)
    
    start_distress = t_event + pd.offsets.BusinessDay(n=1) #usiamo i giorni di trading effettivi 
    end_distress   = t_event + pd.offsets.BusinessDay(n=post_event_days)

    
    df_normal = df_returns.loc[start_normal:end_normal].copy()
    df_distress = df_returns.loc[start_distress:end_distress].copy()

    return df_normal, df_distress

# %%
def calculate_historical_var(df_returns, alphas=[0.01, 0.05]):
    """
    Calcola il VaR Storico per più livelli di confidenza e più titoli contemporaneamente
    """
    var_results = df_returns.quantile(alphas)
    var_results.index.name = "Alpha"
    return var_results.T

# %%
def calculate_expected_shortfall(df_returns, df_var):
    """
    Calcola l'ES basandosi sulla matrice dei VaR precedentemente calcolata.
    Fornire df e matrice VaR corrispondente
    """
    es_results = {}
    for alpha in df_var.columns:
        # Per ogni ticker, calcoliamo la media dei rendimenti < VaR_alpha
        
        es_series = {}
        for ticker in df_returns.columns:
            var_threshold = (df_var.loc[ticker, alpha])
            tail_returns = df_returns[ticker][df_returns[ticker] < var_threshold]
            es_series[ticker] = tail_returns.mean()
        es_results[alpha] = es_series
        
    return pd.DataFrame(es_results)

# %%
from scipy import stats

def get_variations(df_normal, df_distress):
    """Calcola la variazione percentuale tra i due scenari per tutte le colonne."""
    return (df_distress - df_normal) / df_normal

def test_kupiec(df_returns, df_var, p=0.01):
    """
    Test di Kupiec (POF).
    df_var deve essere una Serie o un DataFrame con lo stesso indice di colonne di df_returns.
    """
    N = len(df_returns)
    # Calcolo violazioni per ticker
    n_violazioni = (df_returns < df_var[p].reindex(df_returns.columns)).sum()
    
    p_hat = n_violazioni / N
    
    # Likelihood Ratio 
    
    term1 = (N - n_violazioni) * np.log((1 - p) / np.maximum(1 - p_hat, 1e-10)) #per gestionedi log(0) e /0 = ERROR 
    term2 = n_violazioni * np.log(p / np.maximum(p_hat, 1e-10))
    LR = -2 * (term1 + term2)
    
    # p-value
    p_values = 1 - stats.chi2.cdf(LR, df=1)
    
    return pd.DataFrame({'Violazioni': n_violazioni, 'p-value': p_values}).T


