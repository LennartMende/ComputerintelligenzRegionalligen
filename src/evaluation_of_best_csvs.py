import pandas as pd
from pathlib import Path

def evaluation_of_best_csvs():

    # Hauptverzeichnis
    base_path = Path(__file__).resolve().parent.parent / "evaluations"

    # Alle best_data.csv-Dateien in Unterverzeichnissen finden
    for csv_file in base_path.rglob("best_data.csv"):

        # CSV einlesen
        df = pd.read_csv(csv_file)

        # Alle Spalten außer der ersten verwenden
        werte = df.iloc[:, 1:]

        # Mittelwert und Minimum für jede Spalte
        df_ergebnis = pd.DataFrame({
            "mean": werte.mean(axis=0),
            "min": werte.min(axis=0)
        })

        # Ergebnisdatei im gleichen Ordner speichern
        output_file = csv_file.parent / "mean_min.csv"

        df_ergebnis.to_csv(output_file)

        print(f"Verarbeitet: {csv_file}")
        print(f"Gespeichert:  {output_file}")