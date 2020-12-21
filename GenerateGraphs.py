from matplotlib import pyplot as plt

class GenerateGraphs():
    def generate_plots(self, graph_data):
        if len(graph_data["x_axis"]) >= 40:
            plt.figure(figsize=(15,4))
            plt.xticks(rotation=90)
        else:
            plt.xticks(rotation=70)
        plt.plot(graph_data["x_axis"],graph_data["y_axis"])
        plt.title(graph_data["title"])
        plt.show()
        plt.loglog(
            range(len(graph_data["x_axis"])),
            graph_data["y_axis"])
        plt.title(graph_data["title"])
        plt.gca().axes.xaxis.set_visible(False)
        plt.show()
        plt.pie(
            graph_data["y_axis"], 
            labels=graph_data["x_axis"],
            autopct='%1.1f%%', 
            shadow=True, 
            startangle=140)
        plt.title(graph_data["title"])
        plt.axis('equal')
        plt.show()