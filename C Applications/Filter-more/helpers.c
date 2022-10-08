#include "helpers.h"
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for ( int i=0; i < height; i++)
    {
        for ( int j=0; j < width; j++)
        {
            float green = image[i][j].rgbtGreen;
            float red = image[i][j].rgbtRed;
            float blue = image[i][j].rgbtBlue;
            int average=round((blue + green + red)/3);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE reflected;
    for ( int i = 0; i < height; i++)
    {
        for ( int j = 0; j < width/2; j++)
        {
            reflected=image[i][j];
            image[i][j]=image[i][width-(j+1)];
            image[i][width-(j+1)]=reflected;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE blur[height][width];
    for ( int i=0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
           blur[i][j]=image[i][j];
        }
    }
    for ( int i=0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sumBlue = 0;
            float sumRed = 0;
            float sumGreen = 0;
            int count = 0;
            for (int x=-1; x <= 1; x++)
            {
                for (int y=-1; y <= 1; y++)
                {
                    if (i + x < 0 || i + x >= height || j + y < 0 || j + y >= width)
                    {
                        continue;
                    }
                    else
                    {
                        sumRed += blur[i+x][j+y].rgbtRed;
                        sumBlue += blur[i+x][j+y].rgbtBlue;
                        sumGreen += blur[i+x][j+y].rgbtGreen;
                        count++;
                    }
                }
            }
            
                image[i][j].rgbtRed = round(sumRed/count);
                image[i][j].rgbtBlue = round(sumBlue/count);
                image[i][j].rgbtGreen = round(sumGreen/count);
        }
    }
        return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE edge[height][width];
    for ( int i=0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
           edge[i][j]=image[i][j];
        }
    }
    for ( int i=0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float Gx_red = 0;
            float Gx_blue = 0;
            float Gx_green = 0;
            float Gy_red = 0;
            float Gy_blue = 0;
            float Gy_green = 0;
            int red;
            int blue;
            int green;
            int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
            int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
            for (int x=-1; x <= 1; x++)
            {
                for (int y=-1; y <= 1; y++)
                {
                    if (i + x < 0 || i + x >= height || j + y < 0 || j + y >= width)
                    {
                        continue;
                    }
                    else
                    {
                        Gx_red += edge[i+x][j+y].rgbtRed * Gx[x + 1][y + 1];
                        Gx_blue += edge[i+x][j+y].rgbtBlue * Gx[x + 1][y + 1];
                        Gx_green += edge[i+x][j+y].rgbtGreen * Gx[x + 1][y + 1];
                        Gy_red += edge[i+x][j+y].rgbtRed * Gy[x + 1][y + 1];
                        Gy_blue += edge[i+x][j+y].rgbtBlue * Gy[x + 1][y + 1];
                        Gy_green += edge[i+x][j+y].rgbtGreen * Gy[x + 1][y + 1];
                    }
                }
            }
                int square_sum_red = Gx_red * Gx_red + Gy_red * Gy_red;
                int square_sum_blue = Gx_blue * Gx_blue + Gy_blue * Gy_blue;
                int square_sum_green = Gx_green * Gx_green + Gy_green * Gy_green;
                red = round(sqrt(square_sum_red));
                blue = round(sqrt(square_sum_blue));
                green = round(sqrt(square_sum_green));
                if (red > 255)
                {
                    red = 255;
                }
                if (green > 255)
                {
                    green = 255;
                }
                if (blue > 255)
                {
                    blue = 255;
                }
                image[i][j].rgbtRed = red;
                image[i][j].rgbtBlue = blue;
                image[i][j].rgbtGreen = green;
        }
    }
        return;
}

