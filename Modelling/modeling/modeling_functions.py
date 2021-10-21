import pandas as pd
import curveball

def growth_model(x,y,model_name=None,save=False,filename="growthcurve.png"):
    """This function takes the provided (preprocessed) data to plot a growthcurve.


    The model parameter takes an element of curveball.baranyi_roberts_model.
    More information here: https://curveball.yoavram.com/models

    Args:
        x (list): x values (in this case time)
        y (list): y values (in this case optical density)
        model_name (optional): The model parameter takes an element of curveball.baranyi_roberts_model. More information here: https://curveball.yoavram.com/models. Defaults to None.
        save (boolean, optional): if True, the generated figure will be saved. Defaults to False.
        filename (string), optional): filename of the saved figure. Figure will only be saved if save=True. Defaults to "growthcurve.png".
    """
    df = pd.DataFrame(list(zip(x,y)), columns=["Time","OD"])
    print(df.head())
    df = df.dropna()
    models, fig, ax = curveball.models.fit_model(df,PLOT=True,
    PRINT=False, models=model_name)
    if save: fig.savefig(filename)