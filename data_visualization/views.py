from django.shortcuts import render
from .forms import DynamicReportForm  # Updated form name
import plotly.graph_objs as go
from .models import StoredData
from django.urls import reverse

def report(request):
  if request.method == 'POST':
    form = DynamicReportForm(request.POST)
    if form.is_valid():
      # Extract filters and data points from the form
      filters = form.cleaned_data['filters']
      data_points = form.cleaned_data['data_points']  # List of selected data points

      # Retrieve data from data_storage app based on filters
      data = StoredData.objects.filter(**filters)

      # Further filter or process data based on report requirements:
      if data_points:
        # Filter data based on specific data points
        data = data.filter(**{f'{dp}__isnull': False for dp in data_points})

      # Process and format data for Plotly (modify based on your model fields)
      report_data = []
      for item in data:
        data_dict = {}
        for dp in data_points:
          data_dict[dp] = getattr(item, dp)  # Access data point fields dynamically
        report_data.append(data_dict)

      # Create Plotly figure
      processed_data = []
      # Choose chart type and data based on user selections
      for item in report_data:
        x_data = [item['upload_date']]  # Assuming data points have dates
        # Use a dictionary to map data points to chart types and data series creation logic
        chart_types = {
          'data_point_1': go.Bar(name=f'{item["filename"]} - Data Point 1', y=item['data_point_1']),
          'data_point_2': go.Scatter(name=f'{item["filename"]} - Data Point 2', y=item['data_point_2']),
          # ... add more data point mappings
        }
        processed_data.append(chart_types[data_points[0]])  # First data point
        if len(data_points) > 1:  # Add additional traces if multiple points selected
          processed_data.append(chart_types[data_points[1]])

      figure = go.Figure(data=processed_data)
      # ... rest of figure creation logic
      return render(request, 'report.html', {'figure': figure, 'report_url': reverse('report:report')})
  else:
    form = DynamicReportForm()
  return render(request, 'report.html', {'figure': figure, 'report_url': reverse('report:report')})
