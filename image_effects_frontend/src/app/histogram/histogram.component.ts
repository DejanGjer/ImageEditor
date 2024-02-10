import { Component, ViewChild, ElementRef, AfterViewInit, OnInit } from '@angular/core';
import { Chart, ChartOptions } from 'chart.js/auto';
import { ImageEditorService } from '../services/image-editor.service';

@Component({
  selector: 'app-histogram',
  templateUrl: './histogram.component.html',
  styleUrls: ['./histogram.component.css']
})
export class HistogramComponent implements OnInit, AfterViewInit{
  @ViewChild('histogram') chartCanvas!: ElementRef;
  private chart: Chart | null = null
  histogramData: { histogram_data: Array<number>} | null = null;

  constructor(private imageEditorService: ImageEditorService) {}

  ngAfterViewInit(): void {
    this.createChart();
  }

  ngOnInit(): void {
    this.imageEditorService.getHistogramData().subscribe(
      histogramData => {
        this.histogramData = histogramData;
        this.updateChart();
      }
    );
  }

  getRandomInt(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  createChart() {
    // Your data and options for the chart
    console.log("Creating chart")
    console.log(this.histogramData)
    const data = {
      labels: Array.from({ length: 256 }, (_, index) => index),
      datasets: [
        {
          label: 'Histogram',
          data: Array.from({ length: 256 }, () => {return 0}),
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }
      ]
    };

    const options: ChartOptions<'bar'> = {
      responsive: true,
      scales: {
        x: {
          type: 'linear',
          position: 'bottom',
          min: 0, // Set your minimum value
          max: 255 // Set your maximum value
        },
        y: {
          type: 'linear',
          position: 'left',
          min: 0, // Set your minimum value
          suggestedMax: 3000 // Set your maximum value
        }
      }
    };
    

    // Create the chart
    const ctx: CanvasRenderingContext2D = this.chartCanvas.nativeElement.getContext('2d');
    this.chart = new Chart(ctx, {
      type: 'bar', // Change this to the chart type you want (bar, line, etc.)
      data: data,
      options: options
    });
  }

  updateChart() {
    // Update the chart with new data
    if (this.chart === null) {
      console.log("Chart is null")
      return;
    }
    this.chart.data.datasets[0].data = this.histogramData?.histogram_data || Array.from({ length: 256 }, () => {return 0});
    this.chart.update();
  }

}
