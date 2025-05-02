library(shiny)
library(readr)
library(dplyr)

# Load CSV from URL
DATA_URL <- "https://raw.githubusercontent.com/1Ramirez7/net_exports/main/raw_data/2015-2024_trade_balance_all_commodities.csv"
df <- read_csv(DATA_URL)

# Get column names
column_names <- names(df)

# Define UI
ui <- fluidPage(
  h2("CSV Variable Selector with Unique Values"),
  checkboxGroupInput("columns", "Select columns:", choices = column_names),
  uiOutput("unique_values")
)

# Define server logic
server <- function(input, output, session) {
  output$unique_values <- renderUI({
    selected <- input$columns
    if (is.null(selected) || length(selected) == 0) {
      return(p("No columns selected."))
    }
    
    output_blocks <- lapply(selected, function(col) {
      unique_vals <- df[[col]] %>% na.omit() %>% unique() %>% head(300)
      formatted <- as.character(unique_vals)
      
      tagList(
        h4(paste("Unique values for:", col)),
        tags$ul(lapply(formatted, tags$li))
      )
    })
    
    do.call(tagList, output_blocks)
  })
}

# Run the app
shinyApp(ui, server)
