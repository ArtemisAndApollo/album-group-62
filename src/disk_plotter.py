import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from math import cos, sin, pi
import json
import os
import numpy as np
class DiskPlotter():
    def __init__(self, evals: list[dict], filename_attributes: str):
        self.evals = evals
        self.basepath = r"output/plots/"
        self.filename_attributes = filename_attributes
        self.plot_matrix = {
            "levenshtein": (0, 0),
            "s-levenshtein": (0, 1),
            "ws-levenshtein": (0, 2),
            "hamming": (1, 0),
            "s-hamming": (1, 1),
            "ws-hamming": (1, 2),
            "jaro-winkler": (2, 0),
            "s-jaro-winkler": (2, 1),
            "ws-jaro-winkler": (2, 2),
            "soundex": (-1, -1),
            "weaker-soundex": (-1, -1)
        }

    def _get_single_mode_parameters(self, data: dict = None) -> tuple:
        precision = data["precision"]
        recall = data["recall"]
        f1_score = data["F1-score"]
        
        labels = ['precision', 'recall', 'F1-score']
        sizes = [precision, recall, f1_score]
        mode = data["mode"]
        return (labels, sizes, mode)

    def plot_single_sim_mode(self, save_fig: bool = True, show_fig: bool = False, filename: str = None, data: dict = None):
        if data is not None:
            labels, sizes, mode = self._get_single_mode_parameters(data)
            
            title = f"Comparing precision, recall and F1-score ({mode})"
            filename = filename if filename else f"plot_single_sim_mode-{mode}_{self.filename_attributes}"

            self._plot_bar(
                save_fig=save_fig,
                show_fig=show_fig,
                labels=labels,
                sizes=sizes,
                filename=filename,
                title=title,
                colors=["#cccccc", "#b7b7b7", "#8dd8d3"]
            )

    def plot_all_single_sim_mode(self):
        for eval in self.evals:
            self.plot_single_sim_mode(save_fig = True, show_fig = False, data = eval)
    
    def plot_all_sim_modes_vertical(self, save_fig: bool = True, show_fig: bool = False, filename: str = None):
        fig, ax = plt.subplots()
        filename = filename if filename else f"plot_all_sim_modes_vertical_{self.filename_attributes}"

        f1_scores_dict = self._get_f1_score_with_mode()
        labels, sizes = self._get_lables_sizes(f1_scores_dict)
        title = f"F1-score comparison ({self.filename_attributes.replace("-", ", ")})"

        colors = ['#8dd8d3'] + ['#CCCCCC'] * (len(sizes) - 1)

        bars = ax.bar(labels, sizes, color=colors)

        for bar, value in zip(bars, sizes):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() - 0.15,
                f"{value:.3f}",
                ha="center", 
                va="bottom", 
                fontsize=12,
                weight="bold",
                color="white",
                rotation=90
            )

        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        
        self._disable_top_right_spine(ax)
        ax.set_ylabel("F1-score")
        ax.set_title(title)
        if save_fig: fig.savefig(self.basepath + filename + ".png", bbox_inches='tight')
        if show_fig: plt.show()

    def plot_all_sim_modes_horizontal(self, save_fig: bool = True, show_fig: bool = False, filename: str = None):
        fig, ax = plt.subplots()
        filename = filename if filename else f"plot_all_sim_modes_horizontal_{self.filename_attributes}"

        f1_scores_dict = self._get_f1_score_with_mode()
        labels, sizes = self._get_lables_sizes(f1_scores_dict)
        title = f"F1-score comparison ({self.filename_attributes.replace("-", ", ")})"

        colors = ['#8dd8d3'] + ['#CCCCCC'] * (len(sizes) - 1)

        ax.barh(labels, sizes, color=colors)

        for i, size in enumerate(sizes):
            ax.text(size - 0.08, i, f"{size:.3f}", color='white', va='center', fontsize=13, weight="bold")

        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, ha='right')
        ax.set_xlim(0.4, 1)
        ax.invert_yaxis()
        
        self._disable_top_right_spine(ax)
        ax.set_xlabel("F1-score")
        ax.set_title(title)
        plt.tight_layout()
        if save_fig: fig.savefig(self.basepath + filename + ".png", bbox_inches='tight')
        if show_fig: plt.show()

    def _get_f1_score_with_mode(self) -> dict:
        f1_scores_dict = {}
        for eval in self.evals:
            f1_scores_dict[eval["mode"]] = eval["F1-score"]
        
        return f1_scores_dict
    
    def _get_lables_sizes(self, f1_scores_dict: dict) -> tuple:
        sorted_items = sorted(f1_scores_dict.items(), key=lambda x: x[1], reverse=True)

        labels = [label for label, _ in sorted_items]
        sizes = [score for _, score in sorted_items]

        return (labels, sizes)
    
    def plot_all_sim_modes_subplot_excluded_soundex(self, save_fig: bool = True, show_fig: bool = False, filename: str = None):
        fig, axs = plt.subplots(3,3, sharey=True, sharex=True)
        filename = filename if filename else f"plot_all_sim_mode_subplot_excluded_soundex_{self.filename_attributes}"
        title = f"Comparison of recall, precision and F1-score (all modes) [{self.filename_attributes.replace("-", ", ")}]"

        top_modes = self._get_top_mode_per_row()

        for mode in self.plot_matrix.keys():
            if mode != "soundex" and mode != "weaker-soundex":
                eval = next((d for d in self.evals if d["mode"] == mode), None)
                if eval is not None:
                    labels, sizes, _ = self._get_single_mode_parameters(eval)
                    x, y = self.plot_matrix[mode]
                    
                    if mode in top_modes:
                        axs[x,y].barh(labels,sizes,color=["#cccccc", "#b7b7b7", "#8dd8d3"])
                    else:
                        axs[x,y].barh(labels,sizes,color=["#cccccc", "#b7b7b7", "#a7a7a7"])
                    axs[x,y].set_title(mode, fontsize=10)
                    for i, size in enumerate(sizes):
                        axs[x,y].text(size - 0.35, i, str("{0:.3f}".format(size)), color='white', va='center')
                    
                    self._disable_top_right_spine(axs[x,y])
        
        fig.suptitle(title)
        if save_fig: fig.savefig(self.basepath + filename + ".png", bbox_inches='tight')
        if show_fig: plt.show()

    def _get_top_mode_per_row(self) -> list[str]:
        rows = ["levenshtein", "hamming", "jaro-winkler"]
        top_modes = []

        for row in rows:
            category = [item for item in self.evals if row in item["mode"]]
            category.sort(key=lambda x: x["F1-score"], reverse=True)
            top_modes.append(category[0]["mode"])
        
        return top_modes

    def _plot_bar(self, save_fig: bool = True, show_fig: bool = False, labels: list[str] = None, sizes: list[str] = None, filename: str = None, title: str = None, colors: list[str] = None):
        fig, ax = plt.subplots()
        ax.barh(labels,sizes,color=colors)

        for i, size in enumerate(sizes):
            ax.text(size - 0.15, i, str("{0:.3f}".format(size)), color='white', va='center', fontsize=14)

        self._disable_top_right_spine(ax)
        self._default_plot(ax, fig, title, save_fig, show_fig, filename)


    def plot_single_timing(self, save_fig: bool = True, show_fig: bool = False, filename: str = None, process_times: dict = None):
        """
        Plot timing per process in pie chart.
        """
        if process_times is not None:
            filtered_times = {k: v for k, v in process_times.items() if k != "total"}
            labels = [label.replace("_", " ") for label in filtered_times.keys()]
            total_time = list(process_times.values())[-1]
            sizes = ["{0:.2f}".format(size) for size in filtered_times.values()]
            explode = (0, 0.1, 0, 0)
            title = f"Process times"
            filename = filename if filename else f"plot_timing_{self.filename_attributes}"

            self._plot_pie(
                save_fig=save_fig,
                show_fig=show_fig,
                labels=labels,
                sizes=sizes,
                explode=explode,
                filename=filename,
                title=title,
                type="float",
                colors=["#c7c7c7", "#8dd8d3", "#cccccc", "#b7b7b7"],
                total=total_time
            )

    def plot_multiple_timing(self, save_fig: bool = True, show_fig: bool = False, filename: str = None):
        fig, ax = plt.subplots()
        filename = filename if filename else f"plot_multiple_timing_{self.filename_attributes}"
        
        data_extraction_times, disk_matcher_times, disk_evaluator_times, disk_merger_times, total_times = self._get_process_times(self.filename_attributes)
        if len(total_times) != 0:
            x = range(len(total_times))

            # data_extraction
            self._scatter_plot(ax, x, data_extraction_times, "#fef1c8", "data extraction", "Avg. data extraction")
            # disk_matcher
            self._scatter_plot(ax, x, disk_matcher_times, "#cbe6ff", "disk matcher", "Avg. disk matcher")
            # disk_evaluator
            self._scatter_plot(ax, x, disk_evaluator_times, "#fec3e1", "disk evaluator", "Avg. disk evaluator")
            # disk_merger
            self._scatter_plot(ax, x, disk_merger_times, "#ffdad5", "disk merger", "Avg. disk merger")
            # total
            self._scatter_plot(ax, x, total_times, "#8dd8d3", "total", "Avg. total")

            self._disable_top_right_spine(ax)
            ax.set_xlabel("Data points")
            ax.set_ylabel("Time (s)")
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            self._default_plot(ax, fig, f"Average time per process [{self.filename_attributes.replace("-", ", ")}]", save_fig, show_fig, filename)

    def _scatter_plot(self, ax: Axes = None, x: list = [], y: list = [], color: str = "#8dd8d3", label_scatter: str = "Data", label_avg: str = "Avg."):
        avg_time = self._avg_time(y)
        ax.scatter(x, y, color=color, label=label_scatter + f" (Avg. {avg_time:.3f})")
        ax.axhline(y=avg_time, color=color, linestyle='--')

    def _avg_time(self, data: list = []) -> float:
        return sum(data)/len(data)
    
    def _get_process_times(self, subfolder: str = "artist-dtitle", max_points: int = 25):
        folder_path = self.basepath + "/timing_files_extended/" + subfolder
        data_extraction_times, disk_matcher_times, disk_evaluator_times, disk_merger_times, total_times = [], [], [], [], []
        
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r", encoding='utf-8') as f:
                    data = json.load(f)

                process_times_seconds = data.get("process_times_seconds")

                data_extraction_times.append(process_times_seconds.get("data_extraction"))
                disk_matcher_times.append(process_times_seconds.get("disk_matcher"))
                disk_evaluator_times.append(process_times_seconds.get("disk_evaluator"))
                disk_merger_times.append(process_times_seconds.get("disk_merger"))
                total_times.append(process_times_seconds.get("total"))

            if len(total_times) >= max_points:
                break

        return data_extraction_times, disk_matcher_times, disk_evaluator_times, disk_merger_times, total_times

    def plot_single_tp_fp_tn_fn(self, save_fig: bool = True, show_fig: bool = False, filename: str = None, data: dict = None):
        if data is not None:
            tp = data["tp"]
            fp = data["fp"]
            tn = data["tn"]
            fn = data["fn"]
            total = data["total"]
            
            labels = ['TP', 'FP', 'FN']
            sizes = [tp, fp, fn]
            explode = (0.1, 0, 0)
            title = f"Comparing true, false positives and negatives ({data["mode"]})"
            filename = filename if filename else f"plot_single_tp_fp_tn_fn_mode-{data["mode"]}_{self.filename_attributes}"

            self._plot_pie(
                save_fig=save_fig,
                show_fig=show_fig,
                labels=labels,
                sizes=sizes,
                filename=filename,
                title=title,
                explode=explode,
                colors=["#8dd8d3", "#cccccc", "#b7b7b7"],
                total=total
            )

    def plot_all_single_tp_fp_tn_fn(self):
        for eval in self.evals:
            self.plot_single_tp_fp_tn_fn(save_fig = True, show_fig = False, data = eval)
    
    def plot_all_tp_fp_tn_fn_subplot(self):
        pass

    def plot_all_tp_fp_tn_fn_subplot_excluded_soundex(self):
        pass

    def plot_all_tp_fp_tn_fn_stacked_bar(self, save_fig: bool = True, show_fig: bool = False, filename: str = None):
        title = f"Comparing true, false positives and negatives (all modes) [{self.filename_attributes.replace("-", ", ")}]"
        filename = filename if filename else f"plot_all_tp_fp_tn_fn_stacked_bar_{self.filename_attributes}"

        

        top_mode = self.evals[0]["mode"]
        ordered_modes = list(self.plot_matrix.keys())
        evals_with_rank = self.evals.copy()

        for eval in evals_with_rank:
            if eval["mode"] in ordered_modes:
                eval["rank"] = self.evals.index(eval) + 1
            else:
                eval["rank"] = -1

        ordered_evals = [next(eval for eval in self.evals if eval["mode"] == mode) for mode in ordered_modes]
        top_mode_index = ordered_modes.index(top_mode)

        data = [
            [eval["rank"] for eval in ordered_evals],
            [eval["tn"] for eval in ordered_evals],
            [eval["tp"] for eval in ordered_evals],
            [eval["fn"] for eval in ordered_evals],
            [eval["fp"] for eval in ordered_evals]
        ]

        columns = ordered_modes
        labels = ["rank", 'TN', 'TP', 'FN', "FP"]

        colors = ["#ffffff", "#ffffff", "#8dd8d3", "#aaaaaa", "#c7c7c7"]
        n_rows = len(data)

        index = np.arange(len(columns)) + 0.3
        bar_width = 0.4

        y_offset = np.zeros(len(columns))

        cell_text = []
        fig, ax = plt.subplots(figsize=(20, 10))
        for row in range(n_rows):
            if row in [2, 3, 4]:
                ax.bar(index, data[row], bar_width, bottom=y_offset, color=colors[row])
                y_offset = y_offset + data[row]
            cell_text.append([str(x) for x in data[row]])

        colors = colors[::-1]
        labels = labels[::-1]
        cell_text.reverse()

        table = plt.table(
            cellText=cell_text,
            rowLabels=labels,
            rowColours=colors,
            colLabels=columns,
            loc='bottom'
        )
        
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        for key, cell in table.get_celld().items():
            cell.set_height(0.05)

        for row in range(len(labels)+1):
            table[(row, top_mode_index)].set_text_props(fontweight='bold')

        plt.ylabel(f"Count of TP / FP / FN per mode")
        plt.subplots_adjust(left=0.2, bottom=0.2)
        plt.xticks([])

        self._default_plot(ax, fig, title, save_fig, show_fig, filename)

    def _plot_pie(self, save_fig: bool = True, show_fig: bool = False, labels: list[str] = None, sizes: list[str] = None, filename: str = None, title: str = None, explode: tuple[float|int] = None, type: str = "int", colors: list[str] = None, total: int|float = None):
        fig, ax = plt.subplots()
        wedges, _ = ax.pie(
            sizes,
            explode=explode,
            startangle=90,
            wedgeprops=dict(width=0.5, edgecolor='w'),
            textprops={'fontsize': 10},
            colors=colors
        )

        self._annotate_pie(ax, wedges, labels, sizes, total, type=type)
        self._default_plot(ax, fig, title, save_fig, show_fig, filename)

    def _annotate_pie(self, ax: Axes = None, wedges: list[Wedge] = None, labels: list[str] = None, sizes: list[str] = None, total: int|float = None, type: str = "int"):
        for i, (wedge, label) in enumerate(zip(wedges, labels)):
            r, t1, t2 = wedge.r, wedge.theta1, wedge.theta2
            theta = (t1 + t2) / 2 % 360
            dr = r * 0.1
            angle = theta * pi / 180

            xc = r / 2 * cos(angle)
            yc = r / 2 * sin(angle)
            
            x1 = (r + dr) * cos(angle)
            y1 = (r + dr) * sin(angle)

            safe_theta = theta
            if safe_theta % 180 == 0:
                safe_theta += 0.1

            connection = f"angle,angleA=0,angleB={safe_theta}"

            if x1 > 0:
                ha = "left"
                x1 = r + 2 * dr
            else:
                ha = "right"
                x1 = -(r + 2 * dr)

            if type == "float":
                label = f"{label} ({float(sizes[i]):.2f}s)"
                center_label = f"total time\n{total:.2f}s"
            elif type == "int":
                label = f"{label} ({int(sizes[i])})"
                center_label = f"total pairs\n{total}"

            if center_label:
                ax.text(0, -0.1, center_label, ha="center", va="center", fontsize=14, weight="bold", color= "#8dd8d3")
            
            ax.annotate(
                label,
                (xc, yc), xycoords="data",
                xytext=(x1, y1), textcoords="data",
                ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", connectionstyle=connection, patchB=wedge)
            )

    def _default_plot(self, ax: Axes = None, fig: Figure = None, title: str = None, save_fig: bool = True, show_fig: bool = False, filename: str = None):
        ax.set_title(title)
        if save_fig: fig.savefig(self.basepath + filename + ".png", bbox_inches='tight')
        if show_fig: plt.show()

    def plot_show_all(self):
        plt.show()

    def _disable_top_right_spine(self, ax: Axes = None):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)