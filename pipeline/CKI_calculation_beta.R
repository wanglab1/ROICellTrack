
##R functions to calculate spatial statistics such as Cross K intersection (CKI) based on the Step2 output.
##Reference: https://www.nature.com/articles/s41467-023-37822-0

library(spatstat)

calculate_Kcross_from_coords <- function(all_cells_coords, green_cells_coords, dist = NULL) {
    # Mark the cells as either 'green' or 'other'
    all_cells_coords$mark <- "other"
    for(i in 1:nrow(green_cells_coords)) {
        all_cells_coords$mark[all_cells_coords$x == green_cells_coords$x[i] & 
                              all_cells_coords$y == green_cells_coords$y[i]] <- "green"
    }
    
    # Window for ppp object
    W <- owin(range(all_cells_coords$x), range(all_cells_coords$y))
    
    # Convert data.frame to ppp object
    ppp_object <- ppp(all_cells_coords$x, all_cells_coords$y, marks = factor(all_cells_coords$mark), window=W)
    
    # Check if ppp_object is multitype
    if(!is.multitype(ppp_object)) {
        stop("Point pattern is not multitype!")
    }
    
    # Calculate Kcross
    r <- seq(0, 100, by=1)
    if (!is.null(dist)) {
        r <- seq(0, dist, by=1)
    }
    
    result <- Kcross(ppp_object, "green", "other", r = r, correction = "border")
    
    return(result)
}


#caculate AUC of Kcross
#code adpated based on https://github.com/bioc/SPIAT/blob/devel/R/AUC_of_cross_function.R
library(pracma)
calculate_AUC_from_Kcross <- function(kcross_result) {
    df.cross <- data.frame(r = kcross_result$r, 
                           border = kcross_result$border,
                           theo = kcross_result$theo)
    # Calculate the difference in AUC using the trapezoidal rule
    AUC <- trapz(df.cross$r, df.cross$border) - trapz(df.cross$r, df.cross$theo)
    
    # Determine the size of the cross k result image
    X <- max(df.cross$r)
    Y <- max(c(df.cross$theo, df.cross$border))
    
    # Normalize the AUC by the total area of the graph
    n_AUC <- AUC / (X * Y)
    
    return(n_AUC)
}

#CKI score (cross-K intersection)
crossing_of_crossK_from_Kcross <- function(kcross_result) {
    # Create df.cross from kcross_result
    df.cross <- data.frame(r = kcross_result$r, 
                           border = kcross_result$border,
                           theo = kcross_result$theo)
    
    # Determine the difference between theo and border
    df.cross$sign <- df.cross$theo - df.cross$border
    
    # Identify where the sign changes (crossing occurs)
    change_of_sign <- diff(sign(df.cross$sign[-1]))
    ix <- which(change_of_sign != 0)
    n <- nrow(df.cross)
    
    # Check if crossing occurs and its position relative to the total distance
    if (length(ix) ==1) {
        first_crossing <- ix[1]
        if (first_crossing/n > 0.04) {
            cat("Crossing of cross K function is detected for this image, indicating a potential immune ring.\n")
            perc <- round(first_crossing/n * 100, 2)
            cat(paste("The first crossing happens at the ", perc, "% of the specified distance.", sep = ""))
            return(perc)
        }
    } 
    
    cat("No valid crossing of cross K function detected.")
    return(NULL)
}

#####################################################################
#read in csv output files from ROICellTrack Step 2
cell_stat<- read.csv("Patient 1 - 03-Up-TuSt Im+.tiff.cell_stat.csv")
colors <- ifelse(cell_stat$G_Int > 15, "red", "black") # Red for G_Int > 15, black otherwise
# Plot with coordinates, reversing the Y-axis (correct if there is vertical flip)
plot(cell_stat$X_coordinate, cell_stat$Y_coordinate, col = colors,
     xlab = "X Coordinate", ylab = "Y Coordinate",
     main = "Spatial Distribution of Cells with G_Int > 15 Highlighted",
     ylim = rev(range(cell_stat$Y_coordinate))) # Reverse the Y axis to correct flip


#load R functions from ROICellTrack github
all_cells_coords <- data.frame(x=cell_stat$X_coordinate,y=cell_stat$Y_coordinate)
green_stat<- cell_stat[cell_stat$G_Int>15,] #cancer cells cutoff
green_cells_coords <- data.frame(x=green_stat$X_coordinate,y=green_stat$Y_coordinate)
kcross_result <- calculate_Kcross_from_coords(all_cells_coords, green_cells_coords)
plot(kcross_result)
auc_value <- calculate_AUC_from_Kcross(kcross_result)
cki_value <- crossing_of_crossK_from_Kcross(kcross_result)






################Other functions##########
#test (random mixed sample )
# Number of points to generate
num_points <- 1000

# Generate random coordinates within specified range
x_coords <- runif(num_points, 0, 1000)
y_coords <- runif(num_points, 0, 1000)
# Assign random labels
labels <- sample(c("green", "other"), num_points, replace = TRUE)

# Create two datasets
all_cells_coords <- data.frame(x = x_coords, y = y_coords, mark = labels)
green_cells_coords <- subset(all_cells_coords, mark == "green")[, c("x", "y")]

head(all_cells_coords)
head(green_cells_coords)

kcross_result <- calculate_Kcross_from_coords(all_cells_coords, green_cells_coords)
plot(kcross_result)

auc_value <- calculate_AUC_from_Kcross(kcross_result)
auc_value
cki_value <- crossing_of_crossK_from_Kcross(kcross_result)


################Other functions##########
generate_moderate_noisy_ring_pattern <- function(center=c(500, 500), inner_radius=120, outer_radius=130, 
                                                num_tumor_cells=700, num_immune_cells=200) {
    # Generate tumor cells with moderate noise around the center
    tumor_angle <- runif(num_tumor_cells, 0, 2*pi)
    tumor_radius <- sqrt(runif(num_tumor_cells)) * outer_radius * 0.5  # moderate spread for tumor cells
    tumor_x <- center[1] + tumor_radius * cos(tumor_angle)
    tumor_y <- center[2] + tumor_radius * sin(tumor_angle)
    
    # Generate immune cells with moderate noise in a ring around the tumor cells
    immune_angle <- runif(num_immune_cells, 0, 2*pi)
    immune_radius <- runif(num_immune_cells, inner_radius, outer_radius)
    # Reduced randomness in radial distance to create moderate noise
    noisy_factor <- rnorm(num_immune_cells, mean=0, sd=2) 
    immune_x <- center[1] + (immune_radius + noisy_factor) * cos(immune_angle)
    immune_y <- center[2] + (immune_radius + noisy_factor) * sin(immune_angle)
    
    # Combine the coordinates
    all_cells_coords <- data.frame(x = c(tumor_x, immune_x), y = c(tumor_y, immune_y), 
                                   mark = c(rep("tumor", num_tumor_cells), rep("immune", num_immune_cells)))
    
    immune_cells_coords <- data.frame(x = immune_x, y = immune_y)
    
    return(list(all_cells_coords = all_cells_coords, immune_cells_coords = immune_cells_coords))
}

# Usage:
simulated_data <- generate_moderate_noisy_ring_pattern()
all_cells_coords <- simulated_data$all_cells_coords
immune_cells_coords <- simulated_data$immune_cells_coords

# Plot the generated data
library(ggplot2)
ggplot(all_cells_coords, aes(x=x, y=y, color=mark)) + 
    geom_point(size=1.5) + 
    coord_fixed(ratio=1) + 
    labs(title="Simulated Moderate Noisy Ring Structure", x="X Coordinate", y="Y Coordinate") +
    theme_minimal() +
    scale_color_manual(values=c("tumor"="red", "immune"="blue"))


head(all_cells_coords)
head(immune_cells_coords)

kcross_result <- calculate_Kcross_from_coords(all_cells_coords, immune_cells_coords)
plot(kcross_result)
auc_value <- calculate_AUC_from_Kcross(kcross_result)
auc_value
cki_value <- crossing_of_crossK_from_Kcross(kcross_result)
