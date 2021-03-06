import numpy as np
import pyvista as pv
from visibilitygraphs.dubinspath import vanaAirplaneCurve
from visibilitygraphs.models import DubinsPathFraction
from enum import IntEnum
"""
Authors
-------
Collin Hague : chague@uncc.edu
"""


class PlotterType(IntEnum):
    UNKNOWN = 0
    DEFAULT = 1
    FRACTION = 2


class SolutionPlotter:
    """
    plots solution to path planning with object avoidance

    Methods
    -------
    plotSolution(environment: PolyData, start: ndarray, end: ndarray, paths: list[DubinsPathFraction])
    """
    def __init__(self, type):
        self.type = type

    def plotSolution(self, environment: pv.PolyData, start: np.ndarray, end: np.ndarray, paths: 'list[DubinsPathFraction]'):
        """
        plots solution to path planning with object avoidance

        Parameters
        ----------
        environment: PolyData
            environment the agent transverses
        start: ndarray
            start orientation of vehicle R^3 x S^2
        end: ndarray
            end orientation of vehicle R^3 x S^2
        paths: list[DubinsPaths]
            list of paths for the vehicle to follow
        """
        plotter = pv.Plotter()
        plotter.add_mesh(environment)
        for path in paths:
            poly = pv.PolyData()
            f = vanaAirplaneCurve(path)
            if self.type == PlotterType.DEFAULT:
                t = np.linspace(0, 1, 100)
            elif self.type == PlotterType.FRACTION:
                t = np.linspace(path.fstart, path.fend, 100)
            points = np.array([f(s) for s in t])
            poly.points = points
            cells = np.full((len(points) - 1, 3), 2, dtype=np.int_)
            cells[:, 1] = np.arange(0, len(points) - 1, dtype=np.int_)
            cells[:, 2] = np.arange(1, len(points), dtype=np.int_)
            poly.lines = cells
            poly['scalars'] = np.arange(poly.n_points)
            mesh = poly.tube(radius=1)
            plotter.add_mesh(mesh)
        s = pv.Sphere(radius=5, center=start[:, :3])
        e = pv.Sphere(radius=5, center=end[:, :3])
        plotter.add_mesh(s, color='green')
        plotter.add_mesh(e, color='red')
        plotter.show()
    
