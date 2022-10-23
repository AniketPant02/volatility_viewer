import dash_bootstrap_components as dbc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np

from .page1 import page1Ret
from .page2 import page2Ret
from .page3 import page3Ret
from .about import aboutPage

def content_meta_populate(pathname, slider_idx):
    
    '''
    
    DATAFRAME CALLS

    '''

    mort_df, vix_df, m_rates, m_vix, corr_coef = fund_rate_corr()
    cpidf = cpi_corr()
    spydf = spy_corr()

    '''
    
    SPY PAGE GRAPH #1
    
    '''

    scatter = pd.merge(spydf, vix_df, how = 'inner', on = 'Date')

    scatter = scatter.set_index(["Date"])
    scatter = scatter.resample("M").mean() 
    scatter.index = pd.to_datetime(scatter.index, format="%Y%m").to_period('M')

    m_ratesSpy = scatter['open'].pct_change()[1:]
    m_vixSpy = scatter['$VIX'].pct_change()[1:]

    vixSpy = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    vixSpy.add_trace(
        go.Scatter(x=spydf["Date"], y=spydf["open"], name="% Change SPY", marker=dict(color="#0D3B66")),
        secondary_y=False
    )

    vixSpy.add_trace(
        go.Scatter(x=vix_df["Date"], y=vix_df['$VIX'], name="VIX Spot ($)", marker=dict(color="#EE964B")),
        secondary_y=True
    )

    # Set x-axis title
    vixSpy.update_xaxes(title_text="Year", title_font_family = "open sans,sans-serif", title_font_size = 11, showgrid= False, ticks="outside", col=1)
    

    # Set y-axes titles
    vixSpy.update_yaxes(title_text="% Change SPY",title_font_family = "open sans,sans-serif", title_font_size = 11, gridcolor='LightGrey', secondary_y=False, showgrid=True, ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    vixSpy.update_yaxes(title_text="VIX Spot ($)",title_font_family = "open sans,sans-serif", title_font_size = 11, gridcolor='LightGrey', secondary_y=True, showgrid=True, ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    vixSpy.update_xaxes(showgrid=False, ticks="outside", col=1, showline=True, linewidth=2, linecolor='black', range=[max(min(spydf['Date']), min(vix_df['Date'])), max(spydf['Date'])])
    vixSpy.update_xaxes(
        rangeslider_visible=True
    )
    vixSpy.update_layout(
    font_family= 'open sans,sans-serif',
    font_size= 11,
    autosize=False,
    width= 850,
    height= 450,
    margin=dict(l=0, r=0, t=30, b=0),
    plot_bgcolor="#FFF",
    title_text="SPY vs. VIX",
    title_font_family = "open sans,sans-serif", title_font_size = 15,
    )
    vixSpy.add_vrect(
        x0="1998-07-16", 
        x1="1998-10-11", 
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    vixSpy.add_vrect(
        x0="2000-03-27", 
        x1="2002-10-09",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    vixSpy.add_vrect(
        x0="2007-10-09", 
        x1="2009-03-09",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    vixSpy.add_vrect(
        x0="2018-10-03", 
        x1="2018-12-24",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    vixSpy.add_vrect(
        x0="2020-02-20", 
        x1="2020-03-23",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)

    '''
    
    SPY PAGE GRAPH #2
    
    '''

    vixSpyScat = px.scatter(x=m_vixSpy, y=m_ratesSpy, color=scatter.index.year[1:], color_continuous_scale=px.colors.sequential.Reds, trendline='ols', trendline_color_override="black")
    vixSpyScat.update_traces(hovertemplate='Amount 1: %{x} <br>Amount 2: %{y}  <br>R^2:'+ str(px.get_trendline_results(vixSpyScat).px_fit_results.iloc[0].rsquared))
    vixSpyScat.update_xaxes(title_text="Monthly Change In ^VIX (%)",title_font_family = "open sans,sans-serif", title_font_size = 11,showgrid= False, gridcolor='LightGrey', ticks="outside", col=1, showline=True, linewidth=2, linecolor='black')
    vixSpyScat.update_yaxes(title_text="Monthly Change In SPY (%)",title_font_family = "open sans,sans-serif", title_font_size = 11,showgrid= True, gridcolor='LightGrey', ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    vixSpyScat.add_hline(line_dash="dash",y=0)
    vixSpyScat.add_vline(line_dash="dash",x=0)
    vixSpyScat.update_layout(
        font_family= 'open sans,sans-serif',
        font_size= 11,
        title_text="Correlation between monthly changes in SPY (%) and ^VIX (%)",
        title_font_family = "open sans,sans-serif", title_font_size = 15,
        autosize=False,
        width= 850,
        height= 450,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="#FFF")
    vixSpyScat.update_layout(coloraxis_colorbar=dict(
                    title="Year",
                ))
    
    '''

    SPY PAGE GRAPH #3

    '''
    
    spyLossGain = make_subplots()
    years = ['Black Monday', 'Gulf War', 'Asia Monetary Crisis', 'Tech Bubble', 'Financial Crisis', 'Trade War', 'COVID-19 Selloff']
    spyLossGain.add_trace(go.Bar(x=years, y=[33.5, 19.9, 19.3, 49.0, 56.8, 19.6, 33.8],
                    base=[-33.5, -19.9, -19.3, -49.0, -56.8, -19.6, -33.8],
                    marker_color='crimson',
                    name='S&P Losses',
                    text = [-33.5, -19.9, -19.3, -49.0, -56.8, -19.6, -33.8],
                    textposition = 'auto'
                    ))
    spyLossGain.add_trace(go.Bar(x=years, y=[21.4, 29.1, 37.9, 33.7, 68.6, 37.1, 77.8],
                    base=0,
                    marker_color='green',
                    name='S&P Recovery',
                    text = [21.4, 29.1, 37.9, 33.7, 68.6, 37.1, 77.8],
                    textposition = 'auto'
                    ))
    spyLossGain.update_yaxes(title_text="% Change in S&P", gridcolor='LightGrey', showgrid=True, ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    spyLossGain.update_xaxes(title_text="Largest S&P Declines", showgrid=False, ticks="outside", col=1, showline=True, linewidth=2, linecolor='black')
    spyLossGain.update_layout(
        font_family= 'open sans,sans-serif',
        font_size= 11,
        title_text="S&P Losses and Gains After Major Events",
        autosize=False,
        width= 400,
        height= 450,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="#FFF",
        legend=dict(
            yanchor="top",
            y=.99,
            xanchor="left",
            x=0.01,
    ))
    spyLossGain.add_hline(y=0)


    '''

    SPY PAGE GRAPH #4

    '''
    colors = ['#E4E4E4'] * 3
    colors[0] = '#51BBFE'
    spyLosses = make_subplots()
    spyLosses = spyLosses.add_trace(go.Bar(x=['Stayed Invested', 'Missed 10 Days', 'Missed 25 Days'], y=[616317, 282358, 134392], marker_color=colors, text = ["$616,317", "$282,358", "$134,392"]))

    spyLosses.update_yaxes(title_text="Money Earned ($)", gridcolor='LightGrey', showgrid=True, ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    spyLosses.update_xaxes(title_text="Investment strategy", showgrid=False, ticks="outside", col=1, showline=True, linewidth=2, linecolor='black')
    spyLosses.update_layout(
        font_family= 'open sans,sans-serif',
        font_size= 11,
        title_text="$100,000 Growth Over Top Performing Days",
        autosize=False,
        width= 400,
        height= 450,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="#FFF",)

    '''

    CPI PAGE GRAPH #1

    '''

    
    scatter = cpidf['Value'].resample("M").mean().pct_change()[1:]
    cpiScat = make_subplots()
    cpiScat.add_trace(
        go.Scatter(x=scatter.index, y=scatter.values, name="CPI", opacity = 0.5, marker=dict(color="#0D3B66"))
    )
    running_mean_cpi = scatter.rolling(6).mean()
    cpiScat.add_trace(
        go.Scatter(x=running_mean_cpi.index, y=running_mean_cpi.values, name="6 month running average", marker=dict(color="#EE964B"))
    )

    cpiScat.update_yaxes(title_text="Increase in CPI per month (%)", gridcolor='LightGrey', showgrid=True, ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    cpiScat.update_xaxes(title_text="Year", showgrid=False, ticks="outside", col=1, showline=True, linewidth=2, linecolor='black')
    cpiScat.update_xaxes(
        rangeslider_visible=True
    )
    cpiScat.update_layout(
        font_family= 'open sans,sans-serif',
        font_size= 11,
        title_text="A century of CPI data, visualized",
        autosize=False,
        width= 850,
        height= 450,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="#FFF",)
    cpiScat.add_vrect(
        x0="1998-07-16", 
        x1="1998-10-11", 
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    cpiScat.add_vrect(
        x0="2000-03-27", 
        x1="2002-10-09",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    cpiScat.add_vrect(
        x0="2007-10-09", 
        x1="2009-03-09",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    cpiScat.add_vrect(
        x0="2018-10-03", 
        x1="2018-12-24",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    cpiScat.add_vrect(
        x0="2020-02-20", 
        x1="2020-03-23",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    
    '''

    CPI PAGE GRAPH #2

    '''
    scatter = pd.merge(vix_df, cpidf, how = 'inner', on = 'Date')
    scatter = scatter.set_index(["Date"])
    scatter = scatter.resample("M").mean() 
    scatter.index = pd.to_datetime(scatter.index, format="%Y%m")

    m_inflation = scatter['Value'].pct_change()[1:]
    m_spy = scatter['$VIX'].pct_change()[1:]
    corr_coef = np.corrcoef(m_inflation, m_spy)[0,1]
    scatter = scatter.reset_index()

    cpiSpy = make_subplots(specs=[[{"secondary_y": True}]])
    cpiSpy.add_trace(
        go.Scatter(x=m_inflation.index, y=m_inflation.values, name="CPI", marker=dict(color="#0D3B66")),
        secondary_y=False
    )
    cpiSpy.add_trace(
        go.Scatter(x=m_spy.index, y=m_spy.values, name="^VIX", marker=dict(color="#EE964B")),
        secondary_y=True
    )
    cpiSpy.update_xaxes(
        rangeslider_visible=True
    )
    cpiSpy.update_xaxes(range=[min(m_inflation.index), max(m_inflation.index)])
    cpiSpy.update_yaxes(title_text="CPI (% MOM)",title_font_family = "open sans,sans-serif", title_font_size = 11, gridcolor='LightGrey', secondary_y=False, showgrid=True, ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    cpiSpy.update_yaxes(title_text="^VIX (% MOM)",title_font_family = "open sans,sans-serif", title_font_size = 11, gridcolor='LightGrey', secondary_y=True, showgrid=True, ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    cpiSpy.update_xaxes(title_text="Year", showgrid=False, ticks="outside", col=1, showline=True, linewidth=2, linecolor='black')
    cpiSpy.update_layout(
        font_family= 'open sans,sans-serif',
        font_size= 11,
        autosize=False,
        width= 850,
        height= 450,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="#FFF",
        title_text="CPI vs ^VIX: monthly changes",
        title_font_family = "open sans,sans-serif", title_font_size = 15,
    )

    cpiSpy.add_vrect(
        x0="1998-07-16", 
        x1="1998-10-11", 
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    cpiSpy.add_vrect(
        x0="2000-03-27", 
        x1="2002-10-09",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    cpiSpy.add_vrect(
        x0="2007-10-09", 
        x1="2009-03-09",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    cpiSpy.add_vrect(
        x0="2018-10-03", 
        x1="2018-12-24",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    cpiSpy.add_vrect(
        x0="2020-02-20", 
        x1="2020-03-23",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)

    '''

    CPI PAGE GRAPH #3

    '''

    cpiSpyScat = px.scatter(x=m_inflation, y=m_spy, color=m_inflation.index.year, color_continuous_scale=px.colors.sequential.Reds, trendline='ols', trendline_color_override="black")
    cpiSpyScat.update_traces(hovertemplate='Amount 1: %{x} <br>Amount 2: %{y}  <br>R^2:'+ str(px.get_trendline_results(cpiSpyScat).px_fit_results.iloc[0].rsquared))
    cpiSpyScat.update_xaxes(title_text="% Increase in ^VIX Per Month",title_font_family = "open sans,sans-serif", title_font_size = 11,showgrid= False, gridcolor='LightGrey', ticks="outside", col=1, showline=True, linewidth=2, linecolor='black')
    cpiSpyScat.update_yaxes(title_text="% Increase in CPI Per Month",title_font_family = "open sans,sans-serif", title_font_size = 11,showgrid= True, gridcolor='LightGrey', ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    cpiSpyScat.add_hline(line_dash="dash",y=0)
    cpiSpyScat.add_vline(line_dash="dash",x=0)
    cpiSpyScat.update_layout(
        font_family= 'open sans,sans-serif',
        font_size= 11,
        title_text="Correlation between monthly changes in CPI (%) and ^VIX ($)",
        title_font_family = "open sans,sans-serif", title_font_size = 15,
        autosize=False,
        height= 450,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="#FFF")
    '''
    
    CPI PAGE GRAPH #4

    '''

    month_corr = 12

    cpiCorr = make_subplots(specs=[[{"secondary_y": True}]])
    cpiCorr.add_trace(
        go.Scatter(x=m_inflation.rolling(month_corr).corr(m_spy).index, y=m_inflation.rolling(month_corr).corr(m_spy),
        name = "CPI/VIX 12-month rolling correlation (r)",
        marker = dict(color="#0D3B66")
        ),
        secondary_y=False
        )
    cpiCorr.add_trace(
        go.Scatter(x=m_inflation.index, y=m_inflation.values, name="Monthly increase in CPI (%)", marker=dict(color="#EE964B")),
        secondary_y=True
    )
    cpiCorr.update_yaxes(title_text="Pearson Correlation (r)", gridcolor='LightGrey', showgrid=True, ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    cpiSpy.update_yaxes(title_text="CPI (% MOM)",title_font_family = "open sans,sans-serif", title_font_size = 11, gridcolor='LightGrey', secondary_y=True, showgrid=True, ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    cpiCorr.update_xaxes(title_text="Year", showgrid=False, ticks="outside", col=1, showline=True, linewidth=2, linecolor='black', range=[min(m_inflation.rolling(month_corr).corr(m_spy).index), max(m_inflation.rolling(month_corr).corr(m_spy).index)])
    cpiCorr.update_layout(
        font_family= 'open sans,sans-serif',
        font_size= 11,
        title_text="12 month rolling correlation of CPI and market volatility (^VIX)",
        autosize=False,
        width= 850,
        height= 450,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="#FFF",
        legend=dict(
            yanchor="bottom",
            y=0.01,
            xanchor="left",
            x=0.01
        )
        )
    cpiCorr.update_xaxes(
        rangeslider_visible=True
    )

    cpiCorr.add_vrect(
        x0="1998-07-16", 
        x1="1998-10-11", 
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    cpiCorr.add_vrect(
        x0="2000-03-27", 
        x1="2002-10-09",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    cpiCorr.add_vrect(
        x0="2007-10-09", 
        x1="2009-03-09",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    cpiCorr.add_vrect(
        x0="2018-10-03", 
        x1="2018-12-24",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    cpiCorr.add_vrect(
        x0="2020-02-20", 
        x1="2020-03-23",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)

    '''
    
    FFR PAGE GRAPH #1

    '''

    ffr = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    ffr.add_trace(
        go.Scatter(x=mort_df["Date"], y=mort_df["rates"], name="Federal Funds Rate (%)", marker=dict(color="#0D3B66"),
        line=dict(
            width=5),
        ),
        
        secondary_y=False
    )

    ffr.add_trace(
        go.Scatter(x=vix_df["Date"], y=vix_df['$VIX'], name="VIX Spot ($)", marker=dict(color="#EE964B")),
        secondary_y=True
    )

    # Set x-axis title
    ffr.update_xaxes(title_text="Year", title_font_family = "open sans,sans-serif", title_font_size = 11, showgrid= False, range=[max(min(mort_df['Date']), min(vix_df['Date'])), max(mort_df['Date'])], ticks="outside", col=1)
    
    ffr.update_xaxes(
        rangeslider_visible=True
    )

    # Set y-axes titles
    ffr.update_yaxes(title_text="Federal Funds Rate (%)",title_font_family = "open sans,sans-serif", title_font_size = 11, gridcolor='LightGrey', secondary_y=False, showgrid=True, ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    ffr.update_yaxes(title_text="VIX Spot ($)",title_font_family = "open sans,sans-serif", title_font_size = 11, gridcolor='LightGrey', secondary_y=True, showgrid=True, ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    ffr.update_xaxes(showgrid=False, ticks="outside", col=1, showline=True, linewidth=2, linecolor='black')
    ffr.update_layout(
    font_family= 'open sans,sans-serif',
    font_size= 11,
    autosize=False,
    width= 550,
    height= 450,
    margin=dict(l=0, r=0, t=30, b=0),
    plot_bgcolor="#FFF",
    title_text="Fed rate changes drive short term volatility",
    title_font_family = "open sans,sans-serif", title_font_size = 15,
    legend=dict(
        yanchor="top",
        y=.97,
        xanchor="left",
        x=0.01,
    )
    )

    ffr.add_vrect(
        x0="1998-07-16", 
        x1="1998-10-11", 
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    ffr.add_vrect(
        x0="2000-03-27", 
        x1="2002-10-09",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    ffr.add_vrect(
        x0="2007-10-09", 
        x1="2009-03-09",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    ffr.add_vrect(
        x0="2018-10-03", 
        x1="2018-12-24",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    ffr.add_vrect(
        x0="2020-02-20", 
        x1="2020-03-23",
        fillcolor="gray",
        opacity=0.2,
        line_width=0)
    
    '''
    
    FFR PAGE GRAPH #2

    '''

    ffrScat = px.scatter(x=m_rates, y=m_vix, color=m_rates.index.year, color_continuous_scale=px.colors.sequential.Reds, trendline='ols', trendline_color_override="black")
    ffrScat.update_traces(hovertemplate='Amount 1: %{x} <br>Amount 2: %{y}  <br>R^2:'+ str(px.get_trendline_results(ffrScat).px_fit_results.iloc[0].rsquared))
    ffrScat.update_xaxes(title_text="Monthly FFR Rate Change (%)",title_font_family = "open sans,sans-serif", title_font_size = 11,showgrid= False, gridcolor='LightGrey', ticks="outside", col=1, showline=True, linewidth=2, linecolor='black')
    ffrScat.update_yaxes(title_text="Monthly VIX Change (%)",title_font_family = "open sans,sans-serif", title_font_size = 11,showgrid= True, gridcolor='LightGrey', ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    ffrScat.add_hline(line_dash="dash",y=0)
    ffrScat.add_vline(line_dash="dash",x=0)
    
    ffrScat.update_layout(
        font_family= 'open sans,sans-serif',
        font_size= 11,
        title_text="Volatility overestimates rate changes",
        title_font_family = "open sans,sans-serif", title_font_size = 15,
        autosize=False,
        width= 300,
        height= 450,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="#FFF",
        coloraxis_colorbar=dict(
            title="Year"
        )
    )

    '''
    
    FFR PAGE GRAPH 3
    
    '''

    month_changes_df = pd.DataFrame()
    month_changes_df['Date'] = m_rates.index
    month_changes_df['month_change_FFR_rates'] = m_rates.values
    month_changes_df['month_change_vix_spot'] = m_vix.values

    bin_month_changes = pd.cut(month_changes_df['month_change_FFR_rates'], bins = 4)

    bins = []
    for bin in bin_month_changes:
        if bin not in bins:
            bins.append(bin)

    month_changes_df['bins'] = bin_month_changes

    avg_df = pd.DataFrame()
    avg_df = month_changes_df.groupby('bins').month_change_vix_spot.mean()

    count_df = month_changes_df.groupby('bins').month_change_vix_spot.count()

    # text=count_df.values

    ffrBar = px.bar(avg_df, x=avg_df.index.categories.astype(str), y=avg_df.values, text=np.round(avg_df.values, 2))
    ffrBar.update_xaxes(title_text="Binned changes in federal fund rates (%)",title_font_family = "open sans,sans-serif", title_font_size = 11,showgrid= False, gridcolor='LightGrey', ticks="outside", col=1, showline=True, linewidth=2, linecolor='black')
    ffrBar.update_yaxes(title_text="Associated monthly change in volatility (%)",title_font_family = "open sans,sans-serif", title_font_size = 11,showgrid= True, gridcolor='LightGrey', ticks="outside", col=1, showline=False, linewidth=2, linecolor='black')
    ffrBar.update_layout(
        font_family= 'open sans,sans-serif',
        font_size= 11,
        title_text="Substantial rate hikes induce portfolio risk via volatility",
        title_font_family = "open sans,sans-serif", title_font_size = 15,
        autosize=False,
        width= 850,
        height= 450,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="#FFF",
        xaxis_tickangle=-45)
    ffrBar.update_traces(marker_color='#0D3B66')

    if pathname == "/":
        if (slider_idx == 0):
            return (
                page1Ret([vixSpy], slider_idx)
            )
        elif (slider_idx == 1):
            return (
                page1Ret([vixSpyScat], slider_idx)
            )
        elif (slider_idx == 2):
            return (
                page1Ret([spyLossGain, spyLosses], slider_idx)
            )
    elif pathname == "/page-2":
        if (slider_idx == 0):
            return (
                page2Ret(cpiScat, slider_idx)
            )
        elif (slider_idx == 1):
            return (
                page2Ret(cpiSpy, slider_idx)
            )
        elif (slider_idx == 2):
            return (
                page2Ret(cpiSpyScat, slider_idx)
            )
        elif (slider_idx == 3):
            return (
                page2Ret(cpiCorr, slider_idx)
            )
    elif pathname == "/page-3":
        if (slider_idx == 0):
            return (
                page3Ret([ffr, ffrScat], slider_idx)
            )
        elif (slider_idx == 1):
            return (
                page3Ret([ffrBar], slider_idx)
            )
    elif pathname == "/about":
        return (
            aboutPage()
        )
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

def fund_rate_corr():
    # RATE TERM: 0.5year, 1year, ..., 30year
    mort_df = pd.read_csv(f'./FEDFUNDS.csv', header = None, names = ['Date', 'rates'], parse_dates = True)
    mort_df['Date'] = pd.to_datetime(mort_df['Date'])
    vix_df = pd.read_csv('./vix-volatility-index-historical-chart.csv', header = None, names = ['Date', '$VIX'])
    vix_df['Date'] = pd.to_datetime(vix_df['Date'])
    
    scatter = pd.merge(mort_df, vix_df, how = 'inner', on = 'Date')

    scatter = scatter.set_index(["Date"])
    scatter = scatter.resample("M").mean() 
    scatter.index = pd.to_datetime(scatter.index, format="%Y%m").to_period('M')

    m_rates = scatter['rates'].pct_change()[1:]
    m_vix = scatter['$VIX'].pct_change()[1:]
    corr_coef = np.corrcoef(m_rates, m_vix)[0][1]
    return mort_df, vix_df, m_rates, m_vix, corr_coef

def cpi_corr():
    vix_df = pd.read_csv('./data/vix-volatility-index-historical-chart.csv', header = None, names = ['Date', '$VIX'], skiprows = 16, parse_dates = True)
    vix_df['Date'] = pd.to_datetime(vix_df['Date'])
    vix_df = vix_df.dropna()
    cpi_df = pd.read_excel("data/cpi/BLS_CPI.xlsx", skiprows = 11)
    cpi_df.columns = cpi_df.columns.str.replace(' ', '')
    cpi_df = cpi_df.drop(['SeriesID'], axis = 1)
    cpi_df['Date'] = pd.to_datetime(cpi_df['Year'].astype(str).str[:-2] + "-" + cpi_df['Period'].str[1:])
    cpi_df = cpi_df.set_index("Date")
    
    return cpi_df

def spy_corr():
    spy_df = pd.read_csv('./MacroTrends_Data_Download_SPY.csv', parse_dates = True)
    spy_df['Date'] = pd.to_datetime(spy_df['date'])

    return spy_df