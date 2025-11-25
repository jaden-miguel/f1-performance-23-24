from __future__ import annotations

import io

import pandas as pd
import pytest
from playwright.sync_api import APIRequestContext, Page, expect

from src import visualization as viz

PLOTLY_DIV_SELECTOR = ".plotly-graph-div"


def wait_for_plotly_render(page: Page):
    page.wait_for_function(
        """(selector) => {
        const el = document.querySelector(selector);
        return Boolean(el && el.data && el.data.length);
    }""",
        arg=PLOTLY_DIV_SELECTOR,
    )


@pytest.mark.e2e
def test_dashboard_renders_plotly_bar_chart(page: Page, static_server: str):
    dashboard_url = f"{static_server}/dist/driver_gap_dashboard.html"
    page.goto(dashboard_url)
    wait_for_plotly_render(page)
    chart = page.locator(PLOTLY_DIV_SELECTOR)
    expect(chart).to_be_visible()

    bars = page.locator("g.barlayer path")
    assert bars.count() > 0, "Expected at least one rendered bar in the Plotly chart."
    bars.first.hover(force=True, position={"x": 2, "y": 2})
    tooltip = page.locator("g.hoverlayer g.hovertext")
    expect(tooltip).to_be_visible()


@pytest.mark.e2e
def test_legend_toggle_updates_traces(page: Page, static_server: str):
    dashboard_url = f"{static_server}/dist/driver_gap_dashboard.html"
    page.goto(dashboard_url)
    wait_for_plotly_render(page)

    def visible_trace_count() -> int:
        return page.evaluate(
            """(selector) => {
            const gd = document.querySelector(selector);
            if (!gd || !gd.data) {
                return 0;
            }
            return gd.data.filter(trace => trace.visible === undefined || trace.visible === true).length;
        }""",
            arg=PLOTLY_DIV_SELECTOR,
        )

    initial_visible = visible_trace_count()
    assert initial_visible > 0, "Expected traces to be visible before toggling the legend."

    legend_entry = page.locator("g.legend g.traces").first
    legend_entry.click()
    page.wait_for_timeout(300)
    after_click = visible_trace_count()
    assert after_click == initial_visible - 1, "Legend toggle should hide one trace."

    legend_entry.click()
    page.wait_for_timeout(300)
    reset_visible = visible_trace_count()
    assert reset_visible == initial_visible, "Second toggle should restore the hidden trace."


@pytest.mark.e2e
def test_chart_matches_filtered_csv_data(
    page: Page,
    static_server: str,
    api_request_context: APIRequestContext,
):
    csv_response = api_request_context.get(f"{static_server}/data/avg_time_gaps.csv")
    assert csv_response.ok
    csv_text = csv_response.text()

    df = pd.read_csv(io.StringIO(csv_text))
    df = df[df["Driver"].isin(viz.driver_meta)].copy()
    df["Team"] = df["Driver"].map(lambda d: viz.driver_meta[d][1])
    df = df[df["Team"] != "Unknown"].copy()
    team_driver_counts = df.groupby(["Team", "Season"])["Driver"].nunique().unstack(fill_value=0)
    team_driver_counts = team_driver_counts.reindex(columns=[2023, 2024], fill_value=0)
    valid_teams = team_driver_counts[(team_driver_counts[2023] == 2) & (team_driver_counts[2024] == 2)].index
    filtered_row_count = len(df[df["Team"].isin(valid_teams)])

    dashboard_url = f"{static_server}/dist/driver_gap_dashboard.html"
    page.goto(dashboard_url)
    wait_for_plotly_render(page)
    rendered_points = page.evaluate(
        """(selector) => {
        const gd = document.querySelector(selector);
        if (!gd || !gd.data) {
            return 0;
        }
        return gd.data.reduce((total, trace) => total + trace.x.length, 0);
    }""",
        arg=PLOTLY_DIV_SELECTOR,
    )

    assert (
        rendered_points == filtered_row_count
    ), "Number of rendered bars should match filtered dataset rows."
