# Nematode Culture Tracker

A dashboard for tracking greenhouse cultures of plant-parasitic nematodes and forecasting when each culture will be ready to harvest.

Nematology labs keep live cultures of species like *Rotylenchulus reniformis*, *Meloidogyne* spp. and *Radopholus similis* on host plants in the greenhouse. Inoculum for experiments comes from these pots. Usually the only record is a tag in the pot, so it is hard to know what is available, how old each culture is, or how many eggs a pot is likely to yield. This app keeps a structured log of every pot and uses the lab's own harvest history to predict yield and harvest timing.

> **Status:** in development. The app currently runs on **simulated data** based on published nematode biology. Real lab records will replace the simulation as they are collected.

## What it does (planned)

- **Culture log:** every pot with its nematode, host, greenhouse, inoculation date and inoculum.
- **Pot status:** age in days and degree-days, and which pots are ready, nearly ready or overdue.
- **Yield model:** eggs per pot as a function of time since inoculation, by nematode × host × greenhouse.
- **Survival model:** the chance a culture is still alive at a given age, since plants sometimes die before harvest.
- **Inventory forecast:** expected eggs available over the coming weeks, with uncertainty.
- **Forecast accuracy:** predicted vs. actual yield for every completed harvest, tracked over time.

## Repository layout

```
app.py                  Streamlit dashboard
src/                    simulation and modelling code
data/                   pots.csv, events.csv, temperatures.csv
docs/DATA_DICTIONARY.md column definitions and allowed values
requirements.txt        Python packages
```

## Running it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Recording real data

See [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md). In short, give each pot a unique ID on its tag, add a row to `pots.csv` when it is inoculated, and add a row to `events.csv` whenever it is harvested, dies or is discarded. **Record egg counts at every harvest, and record plants that die.** Both are what make the forecasts improve.

## Author

Ben Wiseman, Department of Plant and Environmental Protection Sciences, University of Hawaiʻi at Mānoa.

## License

Code: MIT. Data: CC BY 4.0.
