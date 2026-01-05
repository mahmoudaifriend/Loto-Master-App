import plotly.graph_objects as go
import numpy as np

class GlobalLotteryPhysics:
    def __init__(self):
        # Database for USA, Europe, Canada, and UK
        self.game_configs = {
            'Powerball (USA)': {'balls': 69, 'radius': 45, 'gravity': 9.81, 'ink_factor': 0.015},
            'Mega Millions (USA)': {'balls': 70, 'radius': 46, 'gravity': 9.81, 'ink_factor': 0.012},
            'EuroMillions (Europe)': {'balls': 50, 'radius': 50, 'gravity': 9.80, 'ink_factor': 0.018},
            'EuroJackpot (Europe)': {'balls': 50, 'radius': 48, 'gravity': 9.80, 'ink_factor': 0.014},
            'UK Lotto (UK)': {'balls': 59, 'radius': 40, 'gravity': 9.81, 'ink_factor': 0.011},
            'Thunderball (UK)': {'balls': 39, 'radius': 35, 'gravity': 9.81, 'ink_factor': 0.009},
            'Lotto Max (Canada)': {'balls': 50, 'radius': 44, 'gravity': 9.81, 'ink_factor': 0.013},
            'Lotto 6/49 (Canada)': {'balls': 49, 'radius': 42, 'gravity': 9.81, 'ink_factor': 0.010}
        }

    def generate_3d_simulation(self, selected_game):
        cfg = self.game_configs[selected_game]
        n_balls = cfg['balls']
        n_frames = 40  # Simulation frames
        
        # 1. Geometry: Create the Transparent Drawing Drum
        z_cylinder = np.linspace(0, 15, 30)
        theta = np.linspace(0, 2 * np.pi, 30)
        theta_grid, z_grid = np.meshgrid(theta, z_cylinder)
        x_drum = (cfg['radius'] / 10) * np.cos(theta_grid)
        y_drum = (cfg['radius'] / 10) * np.sin(theta_grid)

        # 2. Physics Logic: Ball Trajectories with Mass/Ink Influence
        frames_data = []
        for f in range(n_frames):
            time_step = f * 0.15
            # Random mixing with centrifugal force simulation
            x_pos = np.random.uniform(-3, 3, n_balls) * np.cos(time_step)
            y_pos = np.random.uniform(-3, 3, n_balls) * np.sin(time_step)
            
            # Ink Weight Logic: Higher numbers have slightly more mass (stay lower)
            # Formula: Z_Height = Base_Height / (1 + (Ball_ID * Ink_Factor))
            ball_ids = np.arange(1, n_balls + 1)
            z_pos = np.random.uniform(2, 12, n_balls) / (1 + (ball_ids * cfg['ink_factor']))
            
            frames_data.append(go.Scatter3d(
                x=x_pos, y=y_pos, z=z_pos,
                mode='markers',
                marker=dict(size=9, color=ball_ids, colorscale='Plasma', opacity=0.9,
                            colorbar=dict(title="Ball ID")),
                name=f"Frame {f}"
            ))

        # 3. Assemble the Final Interactive Figure
        fig = go.Figure(
            data=[go.Surface(x=x_drum, y=y_drum, z=z_grid, opacity=0.15, 
                             showscale=False, name="Drum Glass"), 
                  frames_data[0]],
            layout=go.Layout(
                title=dict(text=f"Advanced Physics Simulation: {selected_game}", font=dict(size=20)),
                scene=dict(
                    xaxis=dict(title='Width (cm)'),
                    yaxis=dict(title='Depth (cm)'),
                    zaxis=dict(title='Height (cm)'),
                    aspectmode='manual',
                    aspectratio=dict(x=1, y=1, z=1.4)
                ),
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Run Simulation", method="animate", args=[None])]
                )]
            ),
            frames=[go.Frame(data=[fd], name=str(i)) for i, fd in enumerate(frames_data)]
        )
        return fig

# --- Usage Example (Integration in Streamlit/Web App) ---
# simulator = GlobalLotteryPhysics()
# fig = simulator.generate_3d_simulation('Powerball (USA)')
# fig.show()
