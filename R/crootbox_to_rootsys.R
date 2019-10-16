


crootbox-txt_to_rootsys <- function(input, output){
  
  
  rootsystem <- fread(input, header = T)
  
  
  first <- rootsystem[rootsystem$node1ID == 0,]
  nodals_ids <- unique(rootsystem$branchID[rootsystem$type == 4 | rootsystem$type == 5])
  for(no in nodals_ids){
    temp <- rootsystem[rootsystem$branchID == no][1]
    connection <- data.frame(node1ID = 0,
                             node2ID = temp$node1ID,
                             branchID = temp$branchID,
                             x1 = first$x1, y1 = first$y1, z1 = first$z1,
                             x2 = temp$x1, y2 = temp$y1, z2 = temp$z1,
                             radius = temp$radius,
                             length = sqrt((first$x1-temp$x1)^2 + (first$y1-temp$y1)^2 + (first$z1-temp$z1)^2 ),
                             R = 0, G = 0, B = 0,
                             time = temp$time,
                             type = temp$type)
    rootsystem <- rbind(rootsystem, connection)
  }
  rootsystem <- rootsystem[order(rootsystem$node2ID, decreasing = F),]
  
  
  rs <- rootsystem %>%
    mutate(branchID = branchID+1)
  
  sep <- "     "
  
  ids <- data.frame(branchID=unique(rs$branchID))
  ids$branchID2 <- c(1:nrow(ids))
  
  rs <- rs  %>%
    mutate(order = ifelse(type == 2 | type == 3, 2, 1)) %>%
    mutate(diff_branch = c(0,diff(branchID))) %>%
    mutate(volume = round(2*pi*radius * length, 4)) %>%
    group_by(branchID) %>%
    mutate(cumlength=cumsum(length)) %>%
    mutate(totlength = sum(length)) %>%
    mutate(apex = ifelse(totlength - cumlength == 0, 1, 0)) %>%
    ungroup() %>%
    mutate(apex_id = cumsum(apex)) %>%
    inner_join(ids) %>%
    mutate(branchID = branchID2) %>%
    arrange(branchID, node2ID)
  
  
  # Create a string with the segment values
  segments <- paste0("\t\t", rs$node2ID, sep,
                     rs$x2, sep,
                     rs$y2, sep,
                     rs$z2, sep,
                     rs$node1ID, sep,
                     rs$order, sep,
                     rs$branchID, sep,
                     rs$length, sep,
                     rs$volume, sep,
                     0, "\n",
                     "\t\t", rs$time, "\n",
                     collapse = "")
  
  # Filter the apexes from the global table
  apexes <- rs %>%
    filter(apex == 1) %>%
    arrange(branchID)
  
  # Print the tips values
  tips <- paste0("\t\t", apexes$apex_id, sep,
                 apexes$x2, sep,
                 apexes$y2, sep,
                 apexes$z2, sep,
                 apexes$node2ID, sep,
                 apexes$order, sep,
                 apexes$branchID, sep,
                 apexes$totlength, sep,
                 0, "\n\t\t", 0, sep, 0, "\n", collapse = ""
  )
  
  
  text <- paste0("Time:\n\t\t",max(rs$time),"\n\n")
  text <- paste0(text, "Number of seeds\n\t\t1\n\n")
  text <- paste0(text, "ID, X and Y coordinates of the seeds (one per line)\n\t\t1  0  0\n\n")
  text <- paste0(text, "Root DM, shoot DM, leaf area:\n\t\t0  0  0\n\n")
  text <- paste0(text, "Average soil strength and solute concentration experienced by root system:\n\t\t0  0\n\n")
  text <- paste0(text, "Total # of axes:\n\t\t",length(unique(rs$branchID[rs$order == 1])),"\n\n")
  text <- paste0(text, "Total # of branches, including axis(es):\n\t\t",length(unique(rs$branchID)),"\n\n")
  text <- paste0(text, "Total # of segment records:\n\t\t",nrow(rs),"\n\n")
  text <- paste0(text, "segID#    x          y          z      prev or  br#  length   surface  mass\norigination time\n")
  text <- paste0(text, segments, "\n")
  text <- paste0(text, "Total # of growing branch tips:\n")
  text <- paste0(text, "\t\t", nrow(apexes), "\n\n")
  text <- paste0(text, "tipID#    xg          yg          zg      sg.bhd.tp. ord  br#  tot.br.lgth. axs#\noverlength  # of estblished points\ntime of establishing (-->)\n")
  text <- paste0(text, tips, "\n\n")
  
  cat(text, file = output)
  
}


source("PATH_TO_FILE")
 

library(data.table)
library(tidyverse)

convert_crootbox_rootsys(input = "www/rootsystem.txt", output= "~/Desktop/RootSys")
