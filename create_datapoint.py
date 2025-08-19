#!/usr/bin/python3
"""

Author: Josef Koumar
e-mail: koumajos@fit.cvut.cz, koumar@cesnet.cz

Copyright (C) 2022 CESNET

LICENSE TERMS

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
    1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
    3. Neither the name of the Company nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

ALTERNATIVELY, provided that this notice is retained in full, this product may be distributed under the terms of the GNU General Public License (GPL) version 2 or later, in which case the provisions of the GPL apply INSTEAD OF those given above.

This software is provided as is'', and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed. In no event shall the company or contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.
"""
# Local Application Imports
# from network_time_series import TimeSeries

# Third Part Imports
from cgitb import enable
# import pytrap

MERGER_THRESHOLD = 5


def create_basic_datapoint(
    packets: int,
    bytes: int,
    start_time: float,
    end_time: float,
    label: str = "",
    enable_bytes: bool = True,
):
    """Create datapoint from flow record from NEMEA system.

    Args:
        rec (pytrap.UnirecTemplate): Flow record.

    Returns:
        dict: Datapoint for time series.
    """
    if enable_bytes is True:
        return {
            "packets": packets,
            "bytes": bytes,
            "start_time": start_time,
            "end_time": end_time,
            "label": label,
        }
    else:
        return {
            "packets": packets,
            "start_time": start_time,
            "end_time": end_time,
            "label": label,
        }


def create_time_series(seq, enable_bytes: bool = True):
    """Create time series dictionary for build time series.

    Returns:
        dict: Datapoint for time series.
    """
    if enable_bytes is True:
        return {
            "seq": seq,
            "packets": [],
            "bytes": [],
            "start_time": [],
            "end_time": [],
            "labels": [],
            "sum_flows": 0,
            "sum_packets": 0,
            "sum_bytes": 0,
        }
    else:
        return {
            "seq": seq,
            "packets": [],
            "start_time": [],
            "end_time": [],
            "labels": [],
            "sum_flows": 0,
            "sum_packets": 0,
        }


def append_basic_datapoint(
    datapoint: dict, time_series: dict, enable_bytes: bool = True
):
    time_series["packets"].append(datapoint["packets"])
    if enable_bytes is True:
        time_series["bytes"].append(datapoint["bytes"])
    time_series["start_time"].append(datapoint["start_time"])
    time_series["end_time"].append(datapoint["end_time"])
    time_series["sum_flows"] += 1
    time_series["sum_packets"] += datapoint["packets"]
    if enable_bytes is True:
        time_series["sum_bytes"] += datapoint["bytes"]
    time_series["labels"].append(datapoint["label"])
    


def merge_basic_datapoint(
    datapoint: dict, time_series: dict, enable_bytes: bool = True
):
    time_series["packets"][-1] += datapoint["packets"]
    if enable_bytes is True:
        time_series["bytes"][-1] += datapoint["bytes"]
    time_series["end_time"][-1] = datapoint["end_time"]
    time_series["sum_flows"] += 1
    time_series["sum_packets"] += datapoint["packets"]
    if enable_bytes is True:
        time_series["sum_bytes"] += datapoint["bytes"]


def add_basic_datapoint(
    datapoint: dict,
    time_series: dict,
    enable_bytes: bool = True,
    enable_flow_merger: bool = False,
    exporter_active_timeout: int = 300,
):
    """Add new datapoint to time series.

    Args:
        datapoint (dict): New datapoint.
        time_series (dict): Time series with keys: id, packets, bytes, start_time, end_time.
    """
    if enable_flow_merger is True:
        if len(time_series["end_time"]) == 0:
            last_datapoint_duration = 0
        else:
            if time_series["flow_merge"] is True:
                last_datapoint_duration = exporter_active_timeout
            else:
                last_datapoint_duration = abs(
                    time_series["end_time"][-1] - time_series["start_time"][-1]
                )
        if (
            exporter_active_timeout - MERGER_THRESHOLD
            <= last_datapoint_duration
            <= exporter_active_timeout + MERGER_THRESHOLD
        ):
            time_series["flow_merge"] = True
            merge_basic_datapoint(datapoint, time_series, enable_bytes)
        else:
            time_series["flow_merge"] = False
            append_basic_datapoint(datapoint, time_series, enable_bytes)

    else:
        append_basic_datapoint(datapoint, time_series, enable_bytes)


def build_time_series(
    time_series: dict,
    packets: int,
    bytes: int,
    start_time: float,
    end_time: float,
    label: str = "",
    enable_bytes: bool = True,
    enable_flow_merger: bool = False,
    exporter_active_timeout: int = 300,
):
    """Function take flow record and handl creating and adding new datapoint into time series.

    Args:
        rec (pytrap.UnirecTemplate): Flow record.
        time_series (dict): Time series with keys: id, packets, bytes, start_time, end_time.
    """
    datapoint = create_basic_datapoint(
        packets, bytes, start_time, end_time, label=label, enable_bytes=enable_bytes
    )
    add_basic_datapoint(
        datapoint,
        time_series,
        enable_bytes=enable_bytes,
        enable_flow_merger=enable_flow_merger,
        exporter_active_timeout=exporter_active_timeout,
    )


def proces_flow(
    time_series: dict,
    q_dependencies: list,
    qheuristic: int,
    id_dependency: str,
    packets: int,
    bytes: int,
    start_time: float,
    end_time: float,
    label: str = "",
    enable_bytes: bool = True,
    enable_flow_merger: bool = False,
    exporter_active_timeout: int = 300,
    cutting_timeout: int = 21600,
):
    if id_dependency in q_dependencies:
        time_series[id_dependency]["sum_flows"] += 1
        time_series[id_dependency]["sum_packets"] += packets
        if enable_bytes is True:
            time_series[id_dependency]["sum_bytes"] += bytes
        return
    if id_dependency not in time_series:
        time_series[id_dependency] = create_time_series(0, enable_bytes=enable_bytes)
    if len(time_series[id_dependency]["end_time"]) != 0 and time_series[id_dependency]["end_time"][-1] - time_series[id_dependency]["start_time"][0] > cutting_timeout:
        time_series[f"{id_dependency}___{time_series[id_dependency]['seq']}"] = time_series[id_dependency].copy()
        time_series[id_dependency] = create_time_series(time_series[id_dependency]['seq']+1)
        
    build_time_series(
            time_series[id_dependency],
            packets,
            bytes,
            start_time,
            end_time,
            label=label,
            enable_bytes=enable_bytes,
            enable_flow_merger=enable_flow_merger,
            exporter_active_timeout=exporter_active_timeout,
        )
    if qheuristic != 0 and time_series[id_dependency]["sum_flows"] >= qheuristic:
        q_dependencies.append(id_dependency)
    
