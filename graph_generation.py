import json
import requests
import json


class GraphGenerator:


    def load_json_for_graph(self,input,llm):  
        prompt = (
        f"Analyze the following text and extract any statistical data, if it exists, in the format below:\n\n"
        f"Format Explanation:\n"
        f"[\n"
        f"    {{\n"
        f"        chart_type: (string) The type of chart to create (e.g., 'bar', 'line').\n"
        f"        labels: (list of strings) Categories or regions represented on the x-axis.\n"
        f"        data: (list of objects) Each object contains:\n"
        f"            label: (string) The name of the dataset (e.g., '2022 Sales').\n"
        f"            data: (list of numbers) The values corresponding to each label.\n"
        f"        title: (string) The title of the chart.\n"
        f"        recommended_chart: (string) A recommendation for the best chart type based on the dataset.\n"
        f"    }}\n"
        f"]\n\n"
        f"Example:\n"
        f"[\n"
        f"    {{\n"
        f"        \"chart_type\": \"bar\",\n"
        f"        \"labels\": [\"Region A\", \"Region B\", \"Region C\"],\n"
        f"        \"data\": [\n"
        f"            {{\"label\": \"2022 Sales\", \"data\": [100, 200, 300]}},\n"
        f"            {{\"label\": \"2023 Sales\", \"data\": [150, 250, 350]}}\n"
        f"        ],\n"
        f"        \"title\": \"Sales Comparison Chart\",\n"
        f"        \"recommended_chart\": \"bar\"\n"
        f"    }},\n"
        f"    {{\n"
        f"        \"chart_type\": \"line\",\n"
        f"        \"labels\": [\"January\", \"February\", \"March\"],\n"
        f"        \"data\": [\n"
        f"            {{\"label\": \"Website Traffic\", \"data\": [500, 700, 650]}},\n"
        f"            {{\"label\": \"App Traffic\", \"data\": [300, 400, 450]}}\n"
        f"        ],\n"
        f"        \"title\": \"Monthly Traffic Analysis\",\n"
        f"        \"recommended_chart\": \"line\"\n"
        f"    }}\n"
        f"]\n\n"
        f"Text:\n\n"
        f"{input}"
        "\n Ensure the response is a single JSON array containing all the charts, without extra text or explanations."
        )                                
        try:
            result = llm.invoke(prompt)
            llm_output = result.content.strip()

            print(llm_output)
            # Parse the response content
            response = json.loads(llm_output)
            return self.generate_graph(response)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response from LLM."}
        except Exception as e:
            return {"error": str(e)}
        

    def generate_graph(self, data):
        titles = []
        for chart in data:
            # if len(chart["labels"]) == 0 or len(chart["data"]) == 0:
            #     continue
            chart_config = {
                "type" : chart["type"],
                "data" : {
                    "labels" : chart["labels"],
                    "datasets" : chart["data"]
                },
                "options" : {
                    "title" : {
                        "display" : True,
                        "text" : chart["title"]
                    }
                }
            }
            url = "https://quickchart.io/chart"
            response = requests.post(url, json={"chart": chart_config})
            if response.status_code == 200:
                titles.append(self._save_chart(chart["title"], response.content))
            else:
                print(f"Failed to generate chart. Status code: {response.status_code}")
        return titles

    def _save_chart(self, title, content):
        with open(f"{title}.png", "wb") as file:
            file.write(content)
        print(f"Chart saved as {title}.png")
        return f"{title}.png"


# userInput=""" In a recent survey of 1000 participants, 60% reported regular exercise habits. 
# The average age of participants was 35 years, with a standard deviation of 8 years. 
# Among those who exercised regularly, 70% reported improved sleep quality.
# """
# GraphGenerator().load_json_for_graph(userInput,llm=llm)