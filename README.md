# MixtureAnalyzer
Metric learning for analysis spectral data of mixtures

Spectral methods are an important tool for analyzing the structure and chemical properties of chemical compounds. However, decoding the spectra is
quite a labor-intensive task, and in the case of large signal overlap, identification separate сompound becomes extremely non-trivial.

In this work, a machine learning algorithm was developed to identify chemicals in mixtures based on spectral data. For training and testing
algorithm used a set of model spectra [_J. Schuetzke, N.J. Szymanski, M. Reischl, Comput. Mater. 2023, 9, 100.]_, in which each of the 500 compounds represented by 30 spectra, differing in the degree of broadening of spectral lines, variations in the position of signals and their intensity.
To achieve this goal there was a metric learning approach was used because it allows the algorithm to easily adapt to an increase in the number of classes. At the first stage of the algorithm
high-level latent representations of spectral data are extracted from specta using a convolutional neural network. Then the class of the nearest neighbor in the latent space was assigned to the compound or mixture of the compounds. 
By results of the work, it was possible to develop an algorithm that effectively determines compounds by spectral data both individually and as part of mixtures.
![table](https://sun9-16.userapi.com/impg/7DeCV_dmTrPYk6jOD6rQQDXekMmNt9aZtqUuGA/kWFFw3gj-0I.jpg?size=1081x321&quality=96&sign=945de17258706c0871f3bbe9a94ea9f7&type=album)

You can use https://drive.google.com/file/d/1_Ix5xjDrZR-v6SNT97P-FX5u-y73rtzY/view?usp=sharing to reproduce results.
