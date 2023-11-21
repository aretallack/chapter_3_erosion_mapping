
#####################################
### Return vector of pixel values ###
#####################################

# This function extracts pixel values from a list of provided rasters
# It is designed to take differenced DSMs as the input.

# The function also has a "zones" argument, which expects an sf object of polygons
# with a field named "class", with unique values "flat", "shrub" and "edge".

# If "zones" is not specified, only the first section of the function is run.
# giving a dataframe of pixel values, and a column of the input dataset name for
# each pixel

# If "zones" is specified, the input polygons are use to extract pixels from the 
# input rasters. These extracted pixel values are then output in a dataframe with the 
# dataset name of the input rasters, and the class of the zone polygons. 

# The number of sampled pixels in each class are always equalised to the class
# with the smallest number of pixels to keep sampling balanced.

extract_pixels <- function(rasters, zones) {
  
  names(rasters) <- lapply(rasters, names) %>% 
    unlist()
  
  if (missing(zones)) {
    get_values <- function(rasters) {
      values <- rasters %>% 
        as.data.frame(na.rm = T)
      values <- values %>% 
        add_column(dataset = names(.)[1])
      names(values)[1] <- "value"
      return(values)
    }
    
    values <- lapply(rasters, get_values)
    values <- bind_rows(values)
    values$value <- values$value * 100
    
    return(values)
  
  } else {
    
    extract_byClass <- function(rasters, zones) {
      
      flat_zones <- zones %>% 
        .[which(.$class == "flat"), ]
      shrub_zones <- zones %>% 
        .[which(.$class == "shrub"), ]
      edge_zones <- zones %>% 
        .[which(.$class == "edges"), ]
      
      flat_values <- rasters %>%
        terra::extract(flat_zones, ID = F) %>% 
        unlist() %>%  
        as_tibble() %>% 
        add_column(class = "Flat Surfaces",
                   dataset = names(rasters)) %>% 
      filter(!is.na(value))
        
      shrub_values <- rasters %>%
        terra::extract(shrub_zones, ID = F) %>% 
        unlist() %>%  
        as_tibble() %>% 
        add_column(class = "Vegetation",
                   dataset = names(rasters)) %>% 
        filter(!is.na(value))
      
      edge_values <- rasters %>%
        terra::extract(edge_zones, ID = F) %>% 
        unlist() %>% 
        as_tibble() %>% 
        add_column(class = "Gully Edges",
                   dataset = names(rasters)) %>% 
        filter(!is.na(value))
      
      least <- lapply(list(flat_values, shrub_values, edge_values), nrow) %>%
        unlist() %>%
        min()

      if (least > 0) {
        flat_values <- flat_values[sample(1:nrow(flat_values), least),]
        shrub_values <- shrub_values[sample(1:nrow(shrub_values), least),]
        edge_values <- edge_values[sample(1:nrow(edge_values), least),]
        }
      
      class_values <- rbind(flat_values, shrub_values, edge_values)
      return(class_values)
      
    }
    
    class_values <- lapply(rasters, extract_byClass, zones = zones)
    class_values <- bind_rows(class_values)
    class_values$value <- class_values$value * 100
    
    return(class_values)
  }
  
}


#############################
### Density Plot Function ###
#############################

# Function takes a dataframe of pixel values, Usually from extract_pixels, above
# and creates overlapping density plots of input values using ggridges::

# Arguments include the fields in the input dataframe to use as the x and y axes.

# Scale is an inbuilt argument of geom_density_ridges and controls the overlap of 
# density plots.

# colour_by specifies the field in data that should be used to colour 
# density plots. i.e. grouping variable that should be used for colouring.

# xlim controls the x limits of the plot in the format of c(xmin, xmax)

plot_stats <- function(data, x, y, scale, colour_by, xlim){
  line_width <- 1.25 # Density plot line width
  line_colour <- "grey20" # density plot line colours
  transparency <- 0.8 # Density plot transparency
  text_size <- 25 # Axis text size
  axis_text_size <- 25

  plot <- ggplot(data, aes(x = {{x}}, y = {{y}}, fill = {{colour_by}})) +
    ggridges::geom_density_ridges2(rel_min_height = 0.005, scale = scale, 
                                   quantile_lines = T, quantiles = c(0.05, 0.5, 0.95), 
                                   alpha = 1,
                                  size = 0, # Duplicated plot for legend
                                  colour = NA, # with no colour
                                  show.legend = T) + 
     ggridges::geom_density_ridges2(rel_min_height = 0.005, scale = scale, 
                                   quantile_lines = T, quantiles = c(0.05, 0.5, 0.95), 
                                   alpha = transparency,
                                  size = line_width,
                                  colour = line_colour,
                                  show.legend = F) +
      geom_vline(xintercept = 0, 
                 linewidth = 1.5,
                 colour = "grey30",
                 linetype = "dashed") +
      scale_fill_brewer(palette = "PiYG") +
      theme_classic() +
      theme(strip.background = element_blank(),
            strip.text = element_text(colour = NA),
            axis.text = element_text(size = text_size),
            axis.title = element_text(size = axis_text_size),
            axis.title.x = element_text(margin = margin(t = 20)),
            axis.text.x = element_text(margin = margin(t = 10)),
            axis.title.y = element_blank(),
            axis.text.y = element_blank(),
            axis.ticks.y = element_blank(),
            axis.line.y = element_blank(),
            legend.key.height = unit(0.5, "cm"),
            legend.key.width = unit(1, "cm"),
            legend.position = c(0.7, 0.04),
            legend.direction = "horizontal",
            legend.background = element_rect(fill = "transparent"),
            legend.text = element_text(size = text_size),
            legend.title = element_text(size = text_size, face = "bold"),
            plot.margin = unit(c(t = 10, r = 0, l = 0, r = 0), "mm")) +
    guides(fill = guide_legend(title.vjust = 0.5)) + # Fix legend title justification
      xlab("Elevation difference (cm)") +
      xlim(xlim) 
  return(plot)
}



##################################
### Elevation Profile Function ###
##################################

# requires that an sf object of transects - named "transects" - is present 
# in the environment, with transect names in the second column. 

# Takes a vector of raster DSM paths and the name of the transect to be used in the
# "transects" sf dataframe.

# option: return_values. if TRUE, function returns a dataframe of distances and 
# elevation values to allow independant creation of an elevation profile.
# otherwise, function returns a ggplot of the elevation profile along the 
# provided transect - profiles for each input raster are plotted together.

create_elevation_profile <- function(raster_paths, transect_name, return_values) {
  
  if (missing(return_values)) {
    return_values <- FALSE
  }
  
  transect <- which(as_tibble(transects)[,2] == transect_name) %>% 
    transects[., ]
  
  ##############################################################
  ### Load rasters and project to lowest pixel size of stack ###
  ##############################################################
  
  # load rasters separately as list
  # not as stack as resolutions don't yet match
  tmp_rast <- lapply(raster_paths, rast)
  
  # select highest resolution raster
  # determined by the product of x and y cell sizes
  # used to resample all other rasters
  highest_res <- lapply(tmp_rast, 
                        \(x) res(x) %>% prod()) %>%  # get cell area (product)
    unlist() %>% 
    {which(. == min(.))} %>% # index of highest resolution raster
    tmp_rast[[.]] # select highest resolution raster
  
  # re-project raster stack to the highest res raster
  rasters <- lapply(tmp_rast, # x = list of rasters to project
                    \(x, y) project(x, y),
                    highest_res) %>% # y = project to highest resolution raster
    rast() # Convert list output to raster stack
  
  ########################################
  ### extract elevation profile values ###
  ########################################
  
  # get values for first raster
  values <- terra::extract(rasters[[1]], vect(transect)) %>%
    select(2) # don't need ID column
  
  # get values for successive rasters
  # starting at 2
  for (i in 2:dim(rasters)[[3]]) {
    values <- terra::extract(rasters[[i]], vect(transect)) %>% 
      select(2) %>% 
      cbind(values, .) # continually bind cols to values dataframe
  }
  
  #############################################################
  ### Calcuate distances of extracted values along transect ###
  #############################################################
  
  # Extract values from raster with xy = TRUE to get coords
  first_point <- transect %>%
    st_geometry() %>% 
    st_cast("POINT") %>% 
    .[1]
  
  distances <- terra::extract(rasters[[1]], vect(transect), xy = T) %>% 
    st_as_sf(., coords = c("x", "y")) %>% # Create sf object from xy
    st_geometry() %>% # convert to geometry
    lapply(first_point, #  point at start of transect
           \(x, y) st_distance(y, x), # dist from start (x) to all pixels (y)
           .) %>% # y = all pixel coordinates along line
    unlist()
  
  # add distances to new column in values dataframe
  values <- values %>% 
    add_column(distance = distances, .after = 0)
  
  # pivot longer for plotting
  values <- values %>% 
    pivot_longer(2:ncol(.), names_to = "dataset", values_to = "elevation")
  
  # Normalise values to minium of all rasters
  values$elevation <- values$elevation - min(values$elevation)
  
  if (!return_values) {
  
  ###############################
  ### plot elevation profiles ###
  ###############################
  
  plot <- ggplot(values) +
    # Plain black line plots behind coloured line (outline)
    # geom_line(aes(x = distance, y = elevation, group = dataset),
    #           lwd = 1.2) +
    # Lines coloured by dataset
    geom_line(aes(x = distance, y = elevation, colour = dataset),
              lwd = 0.3) +
    scale_colour_brewer(palette = "PiYG") +
    labs(x = "Distance (m)",
         y = "Elevation (m)",
         colour = NULL) + # No legend title
    theme_classic() +
    theme(
      legend.position = "bottom"
    ) +
    scale_y_continuous(breaks = seq(0, max(values$elevation) + 0.1, by = 0.2))
  
  return(plot)
  } else {
    return(values)
    }
}

