# first week
7<sup> th </sup>-11<sup> th </sup> March 2022

---
## <span style="color:black"> __General information about the data__ </span>
<span style="color:grey">

### __Information about particulate matter (PM) pollution__

* PM is the most harmful air pollution
* PM consists of different types of particles:
    * PM10 = inhalable coarse particles with diameter < 10 µm
    * PM2.5 = fine particles with diameter < 2.5 µm
    * ultrafine particles have a diameter < 0.1 µm
* The European Union has established the European emission standards, which include limits for particulates in the air, see [European Air Quality Index](https://www.eea.europa.eu/themes/air/air-quality-index)
* impacts on PM:
    * smoking, BBQ
    * fireworks (Silvester)
    * dust
    * pollen (PM10)
    * Sahara sand

### __Literature / Links__

* [Exploring the relationship between air pollution and meteorological conditions in China under environmental governance](https://www.nature.com/articles/s41598-020-71338-7): "The concentration of air pollutants at most stations was significantly negatively correlated with wind speed, precipitation and relative humidity, but positively correlated with atmospheric pressure. As the latitude increases, the impact of temperature on the concentration of air pollutants becomes more obvious."
* [Download of air quality data](https://discomap.eea.europa.eu/map/fme/AirQualityExport.htm): more data for Europe
* [Assessment of Measurement Uncertainties for a SDS011 low-cost PM sensor](http://www.opengeiger.de/Feinstaub/SDSFunct.pdf)



## <span style="color:black"> __Data cleaning__ </span>
<span style="color:grey">

### __Open questions__

* Shall we keep the high temperature data (up to 60°C)? Could be relevant per making models per location.

### __standard deviation (std)__

We calculate the std together with mean values per hour. 
* std equals NaN, if 0-1 values are available for mean value calculation
* std equals 0, if only identical values are available for mean value calculation. As this is not probable for a measurement, std == 0 can be taken to find sensor failures.

### __id__

* we drop all kinds of ids (also location) during data merging
* we sum up the measurements based on longitude and latitude > location instead of sensor (position)
* we create a new id during EDA for plotting purpose 

### __sensor failures__

We had long discussions about how to handle presumable sensor failures. For example the PM-sensor yields constant 999.9/1999.9 or 0.0 for long times. We were thinking about replacing every 999.9, 1999.9 and 0.0 with Nan, which would have resulted in minor errors during the calculation of mean values per hour. Finally we decided to calculate the mean values with the data given and to remove sensor failures based on standard deviation (see above). This way we'll get slightly errors for the mean values immediately before or after sensor failures for at least one hour.

---
## <span style="color:black"> __Feature engineering__ </span>
<span style="color:grey">

### __missing values__

* result from
    * missing data
    * data cleaning (expected to be sensor failures)
* to have a continuous time series we plan to 
    * create a DataFrame with rows for every hour and location
    * to a left join with the preprocessed DataFrame
    * impute the missing values
* [juanitorduz/btsa](https://github.com/juanitorduz/btsa/tree/master/python/fundamentals/notebooks): example how to handle missing values

---
## <span style="color:black"> __Modeling__ </span>
<span style="color:grey">

### __Open questions__

* Do we wanna predict PM per city or per location? If we predict per location and keep the high temperatures (up to 60°C) the consideration of sun shine hours (Deutscher Wetterdienst) could be interesting

### __Literature / Links__

* [AutoViML/Auto_TS](https://github.com/AutoViML/Auto_TS): Automatically build multiple Time Series models using a Single Line of Code. 
* [H3: Uber’s Hexagonal Hierarchical Spatial Index](https://eng.uber.com/h3/)
* [mmotl/lnl_biketheft](https://github.com/mmotl/lnl_biketheft): example for usage of Keppler
* [Nixtla/statsforecast](https://github.com/Nixtla/statsforecast): StatsForecast offers a collection of widely used univariate time series forecasting models, including exponential smoothing and automatic ARIMA modeling optimized for high performance using numba


