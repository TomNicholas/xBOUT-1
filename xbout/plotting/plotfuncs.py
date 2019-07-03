import matplotlib.pyplot as plt

from .utils import _decompose_regions


def contourf(da, ax=None, **kwargs):
    """
    Plots a 2D filled contour plot, taking into account branch cuts (X-points).

    Wraps `xarray.plot.contourf`, so automatically adds a colorbar and labels.

    Parameters
    ----------
    da : xarray.DataArray
        A 2D (x,y) DataArray of data to plot
    ax : Axes, optional
        A matplotlib axes instance to plot to. If None, create a new
        figure and axes, and plot to that
    **kwargs : optional
        Additional arguments are passed on to xarray.plot.contourf

    Returns
    -------
    artists
        List of the contourf instances
    """

    # TODO generalise this
    x = kwargs.pop('x', 'R')
    y = kwargs.pop('y', 'Z')

    if len(da.dims) != 2:
        raise ValueError("da must be 2D (x,y)")

    if ax is None:
        fig, ax = plt.subplots()

    regions = _decompose_regions(da)
    region_kwargs = {}

    # TODO create colorbar using all the data?

    # Plot all regions on same axis
    first, *rest = regions
    artists = [first.plot.contourf(x=x, y=y, ax=ax,
                                   **kwargs, **region_kwargs)]
    if rest:
        for region in rest:
            artist = region.plot.contourf(x=x, y=y, ax=ax,
                                          add_colorbar=False, add_labels=False,
                                          **kwargs, **region_kwargs)
            artists.append(artist)

    return artists