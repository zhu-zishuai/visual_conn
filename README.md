# visual_conn
This function allows you to visualize brain source-level connectivity based on an AAL template.

Input format: plot(conn_positive, conn_negative, title)
* conn_positive and conn_negative should be 116-by-116 numpy array, where 116 is the number of ROIs in AAL template

This function was written in Python, and following dependencies are needed:
* Numpy
* Pandas
* Bokeh

Drivers: Visualization result will be exported from html and saved as PNG file, so GeckoDriver or ChromeDriver are needed, You can install these dependencies from Conda as follows:
* For Selenium with GeckoDriver: conda install selenium geckodriver -c conda-forge
* For Selenium with ChromeDriver: conda install selenium python-chromedriver-binary -c conda-forge
* Go to https://docs.bokeh.org/en/latest/docs/user_guide/export.html for details


