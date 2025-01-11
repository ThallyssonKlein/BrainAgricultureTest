import React from "react";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

interface PieChartProps {
  labels: string[];
  data: number[];
  onSliceClick?: (data: string) => void;
}

export default function PieChart({ labels, data, onSliceClick }: PieChartProps) {
  const generateRandomColors = (count: number) => {
    return Array.from({ length: count }, () =>
      `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(
        Math.random() * 256
      )}, ${Math.floor(Math.random() * 256)}, 0.6)`
    );
  };

  const backgroundColors = generateRandomColors(data.length);
  const borderColors = backgroundColors.map((color) => color.replace("0.6", "1"));

  const chartData = {
    labels: labels,
    datasets: [
      {
        data: data,
        backgroundColor: backgroundColors,
        borderColor: borderColors,
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      tooltip: {
        enabled: true,
      },
    },
    onClick: (_event: any, elements: string | any[]) => {
      if (elements.length > 0 && onSliceClick) {
        const elementIndex = elements[0].index;
        const selectedLabel = labels[elementIndex];
        onSliceClick(selectedLabel);
      }
    },  
  };

  return <Pie data={chartData} options={options} />;
};