city_grid <- function(GMDNR){
  
  area_filter <- filter(st_gg21, GMDNR == GMDNR)
  
  grid <- st_make_grid(area_filter, cellsize = 100, 
                       # offset = c(offset$minX, offset$minY), 
                       square = TRUE)  
  
  grid <- st_sf(grid) 
  grid <- st_cast(grid, "POLYGON")
  
  city <- st_intersection(grid, area_filter)
  rm(grid); gc()
  city$ID <- 1:nrow(city)
  city <- relocate(city, ID)
  
  return(city)
}

zurich <- city_grid(261)
geneva <- city_grid(6621)
basel <- city_grid(2701)
lausanne <- city_grid(5586)
bern <- city_grid(351)