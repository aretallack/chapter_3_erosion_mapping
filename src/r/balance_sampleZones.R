library(sf)
zones <- read_sf("./data/shp/sample_zones.shp") %>% 
  select(-c(Shape_Area))
zones <- zones %>% 
  mutate(area = st_area(geometry))

n_flat_1 <- zones %>% 
  filter(site == 1) %>% 
  filter(class == "flat") %>% 
  nrow()

zones_2 <- zones %>% 
  filter(site == 2) %>% 
  .[sample(1:nrow(.), n_flat_1),]

zones <- zones %>%  
  filter(site != 2)

zones <- zones %>% 
  rbind(., zones_2)

write_sf(zones, "./outputs/shp/sample_zones.gpkg")
