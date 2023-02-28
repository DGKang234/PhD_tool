import numpy as np
import pandas as pd
import plotly.graph_objects as go
from tqdm import tqdm


class GLOBAL_OPTI:
    def __init__(self, a):
        self.a = 1

    def Rosenbrock(x, y, a=0.1, b=100):
        return((a-x)**2 + b*(y - x**2)**2)


    def close_to_any(a, floats, atol_val):
        return np.any(np.isclose(a, floats, atol=atol_val))


    def MAP_ENERGY_LANDSCAPE():
        ''' Grid search on the energy landscape '''
        x_coord, y_coord = np.arange(-5, 5, 0.05), np.arange(-5, 5, 0.05)
        z_coord = []
        for i in x_coord:
            z_y = []
            for j in y_coord:
                z_y.append(GLOBAL_OPTI.Rosenbrock(i, j, 1, 100))
            z_coord.append(z_y)
        z_coord = np.array(z_coord)
        z_coord = np.transpose(z_coord)
        return x_coord, y_coord, z_coord


    def METROPOLIS_MC(no_step):
        ''' Metropolis MC '''

        x_initial, y_initial = np.round(np.random.uniform(-5, 5, size = 2), 7)
        energy_initial = GLOBAL_OPTI.Rosenbrock(x_initial, y_initial, 1, 100)

        x_vec , y_vec , energy_vec = [] , [] , []
        step_cnt = 0

        while step_cnt < int(no_step):
            x_, y_ = np.round(np.random.uniform(-1,1, size = 2), 7)
            x_new, y_new = x_initial + x_, y_initial + y_

            energy_new = GLOBAL_OPTI.Rosenbrock(x_new , y_new)

            delta = energy_new - energy_initial
            energy_tol = np.random.uniform(0,1)
            if energy_tol < np.exp(-delta):
                if (GLOBAL_OPTI.close_to_any(x_new, x_vec, 1e-8) and GLOBAL_OPTI.close_to_any(y_new, y_vec, 1e-8)) == False:
                    x_vec.append(x_new)
                    y_vec.append(y_new)
                    energy_vec.append(energy_new)
                    x_initial, y_initial, energy_initial = x_new, y_new, energy_new
                    step_cnt += 1
            else:
                x_vec.append(x_initial)
                y_vec.append(y_initial)
                energy_vec.append(energy_initial)

            df = pd.concat([pd.DataFrame(x_vec), pd.DataFrame(y_vec), pd.DataFrame(energy_vec)] , axis = 1)
            df.columns=["x","y","Energy"]

        # Get the global minimum 
        min_row = df[df.Energy == df.Energy.min()].iloc[-1]
        #print(list(zip(df[df.Energy == df.Energy.min()]["x"].to_list(), df[df.Energy == df.Energy.min()]["y"].to_list())))
        print("The Optimized Value of x and y ----> ", end="")
        print("%8.6f\t%8.6f" % (min_row["x"], min_row["y"] ), end="")
        print(" respectively")
        return df


    def VIS_ENERGY_LANDSCAPE(df, x_coord, y_coord, z_coord):
        ''' Visualise the energy landscape and optimisation trace '''
        fig = go.FigureWidget()
        fig.add_trace(
            go.Scatter3d(
                x=df["x"],
                y=df["y"],
                z=df["Energy"],
                marker=dict(
                    size=4,
                    color=df["Energy"],
                    colorscale='Viridis',
                ),
                line=dict(
                    color='darkblue',
                    width=2
                )
                ),)

        # Map energy landscape
        #fig.add_trace(go.Surface(
        #            x=x_coord,
        #            y=y_coord,
        #            z=z_coord
        #))

        fig.layout = dict(
            xaxis=dict(
                showgrid=True,
                zeroline=False,
                title="x coordinate"),

            yaxis=dict(
                showgrid=True,
                zeroline=False,
                title="y coordinate"),

            font=dict(size=20))

        fig.update_layout(
            width=1000,
            height=900,
            autosize=False,
            scene=dict(
                zaxis=dict(
                    title="Potential energy",
                nticks=4, range=[0,5],),
                camera=dict(
                    up=dict(
                        x=0,
                        y=0,
                        z=1
                    ),
                    eye=dict(
                        x=0,
                        y=1.0707,
                        z=1.5,
                    )
                ),
                aspectratio = dict( x=1, y=1, z=0.7 ),
                aspectmode = 'manual'
            ),
        )
        fig.write_html("metropolis_MC.html")

if __name__ == '__main__':
    #OPTI = GLOBAL_OPTI()
    x_initial, y_initial = np.round(np.random.uniform(-5, 5, size = 2), 7)
    energy_initial = GLOBAL_OPTI.Rosenbrock(1, 100)
    x_coord, y_coord, z_coord = GLOBAL_OPTI.MAP_ENERGY_LANDSCAPE()
    df = GLOBAL_OPTI.METROPOLIS_MC(200)
    GLOBAL_OPTI.VIS_ENERGY_LANDSCAPE(df, x_coord, y_coord, z_coord)

