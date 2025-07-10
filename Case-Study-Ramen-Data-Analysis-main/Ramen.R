#title: "CaseStudyRamen"
#author: "Krrish Ghindani"
#date: "2024-09-16"

#Loading the data frame
load("//Users/krrishghindanii/Desktop/BSDS100/ramen.Rdata")

#summarize ramen data
summary(ramen)

#how many different brands in the data set
length(unique(ramen$Brand))

#turning Top.Ten data in a string column
ramen$Top.Ten <- as.character(ramen$Top.Ten, rm.na=TRUE)
#subsetting the year
years <- (substr(ramen$Top.Ten,1,4))

#printing unique values for year
print("Years with Top Ten data: ")

unique(years)


#ramen brands from the United States
USA.brands <- which(ramen$Country =='USA','United States')

print("Ramen Brands from the US:")

unique(ramen$Brand[USA.brands])

#subsetting to find place won by winning ramen
rating <- (substr(ramen$Top.Ten,6,7))
#selecting who won first place
top.1.indeces <- which(rating =='#1')
#getting the brands who won first place
top1.brands <- ramen$Brand[top.1.indeces]
#store top1.brands in a table
brand_counts <- table(top1.brands)
#look up for what elements in the list show up more than once
brands_more_than_once <- names(brand_counts[brand_counts >1])
brands_more_than_once

#Aggregating by brands and calculating the mean of each brand
brand.stars.average <- aggregate(ramen$Stars, by = list(ramen$Brand), FUN =
                                   "mean", na.rm=FALSE)
#maximum average
max_average_stars <- max(brand.stars.average$x, na.rm =TRUE)
print(max_average_stars)

#top brands with maximum average rating
top_brand <- brand.stars.average[brand.stars.average$x == max_average_stars,]
print(top_brand$Group.1)


#loading libraries
library(ggplot2)
library(dplyr)
#lead dplyr package to use group by

#grouping by country and style and selecting only countries whose count is greater than 10
packaging_data <- ramen %>% group_by(Country, Style) %>% summarise(Count = n()) %>% filter(Count >10)

#plotting country against count filling bars by style
ggplot(packaging_data, aes(x = Country, y = Count, fill = Style)) + geom_bar(stat =
                                                                               "identity", position ="stack") + 
  labs(title ="Ramen Packaging Styles by Country", x ="Country", y ="Count", fill="Packaging Style") +
  scale_fill_brewer(palette ="Set3"
)

#number of ramen entries for country
country_ramen_count <- ramen %>% group_by(Country) %>% summarize(Ramen_Count = n()) %>% arrange(desc(Ramen_Count))
#selectign the country which produces the most ramen
most_ramen_country <- country_ramen_count %>% slice(1)
print(most_ramen_country)
#Japan with 352 count

# Best ramen = best Stars average
# Group by Country and calculate average stars
country_average_stars <- ramen %>% group_by(Country) %>% summarize(Average_Stars = mean(Stars, na.rm =
                                                                                          TRUE
)) %>% arrange(desc(Average_Stars))
# Find the country with the highest average stars
best_country <- country_average_stars %>% slice(1)
print(best_country) #best country is Brazils


#Another way we thought about "best" ramen
#Best Ramen - country with most nominees in top 10
top.brand <- ramen$Brand[top.1.indeces]
top.countries <- ramen$Country[top.brand]
# countries in top 10 multiple times table with count
country_counts <- table(top.countries)
most_frequent_country <- names(which.max(country_counts))
most_frequent_country


library('ggplot2')
library('tidyr')
#for drop_na() function
#more than 20 as count of style
saltiness <- ramen %>% drop_na() %>% group_by(Style, na.rm=TRUE)
#boxplot of Style and percent salt
ggplot(saltiness, aes(x = Style, y = perc_salt)) + geom_boxplot()

# Filter ramen styles with more than 20 counts and perc_salt greater than 18
more_than_18 <- ramen %>% drop_na() %>% group_by(Style) %>% filter(n() > 20 & perc_salt > 18 )
#plot percent of salt by country
qplot(x = perc_salt, data=more_than_18, colour = Country)

#percent of salt by Style and country
qplot(x = perc_salt, data=more_than_18, facets = .~Style, colour = Country)


#plot percent of salt agaist star rating
qplot(perc_salt, Stars, data = ramen) + geom_smooth(method=lm)

# Scatter plot of perc_salt vs Stars, colored by Style
qplot(perc_salt, Stars, data=ramen, color=Style)

#plot of percent of salt and country
qplot(perc_salt, Country, data=ramen)

summary(ramen$perc_salt)

#creating a subset of more than 22 percent salt
more_than22_salt <- ramen %>% filter(perc_salt >22)
#plotting countries with more than 22% of salt and adding Style
ggplot(more_than22_salt, aes(x = Country, y = perc_salt, fill = Style)) + geom_bar(stat ="identity", position ="stack") + 
  theme(axis.text.x = element_text(angle = 90)) + 
  labs(title ="Ramen Packaging Styles by Country", x ="Country", y ="Count", fill ="Packaging Style") + 
  scale_fill_brewer(palette ="Set3")


# Filter the top 10 brands
top_brands <- ramen %>% 
  count(Brand) %>% 
  top_n( 10, n) %>% 
  pull(Brand)
# plot percentage of salt by brand
ggplot(ramen %>% filter(Brand %in% top_brands), aes(x = Brand, y = perc_salt)) + geom_boxplot() + labs(title = "Distribution of Salt Percentage by Top 10 Ramen Brands", x ="Brand", y ="Percentage of Salt"
)

#loading libraries
library(tidyr)
library(stringr)

estimate_saltiness <- function(variety) {
  # Define keywords that indicate saltiness
  salt_words <- c("salt", "soy", "shoyu", "miso", "seafood", "fish", "shrimp", "crab")      
  salt_score <- sum(str_count(tolower(variety), salt_words))
  return(salt_score)
}

# Add a new column for Saltiness based on the Variety
ramen <- ramen %>% mutate(Saltiness = sapply(Variety, estimate_saltiness))
# Get the top 10 countries with the most ramen varieties
top_countries <- ramen %>% count(Country) %>% top_n(10, n) %>% pull(Country)
# Create a violin plot for the distribution of saltiness in the top coumntries
ramen %>% filter(Country %in% top_countries) %>% ggplot(aes(x = Country, y = Saltiness, fill = Country)) + geom_violin() + labs(title =
                                                                                                                                  "Distribution of Estimated Saltiness by Country",                                                                                                                                x ="Country",
                                                                                                                                y ="Estimated Saltiness"
)

#break down ramen into 5 collections of “similar” ramens
# Let's create 5 categories based on Stars rating and perc_salt
max(ramen$perc_salt)

min(ramen$perc_salt)

ramen$Collection <- ifelse(ramen$perc_salt <=5, "Very Low Salt",          ifelse(ramen$perc_salt > 5 & ramen$perc_salt <= 10, "Low Salt", ifelse(ramen$perc_salt >10 & ramen$perc_salt <=15,"Average Salt", ifelse(ramen$perc_salt >15 & ramen$perc_salt <=20, "High Salt", ifelse(ramen$perc_salt >20 & ramen$perc_salt <= 25, "Premium High Salt", "Ultra Premium High Salt"
))))) 
category_counts <- table(ramen$Collection)
#Plotting percent of salt and stars and coloring by collection (level of saltiness)
qplot(x = perc_salt, y = Stars, data = ramen, color = Collection)


#Analyzing only the Premium High Saltiness
premium_high_salt <- ramen %>% filter(Collection ==
                                        "Premium High Salt")
premium_high_salt$Style <- as.factor(premium_high_salt$Style)
#boxplot of style and stars of only premium high salt
qplot(x = Style, y = Stars, data = premium_high_salt) + geom_boxplot()

#loading libraries
library('readr')

#Another way to break down our data set in 5 categories is based on the star rating
ramen$Stars <- as.numeric(ramen$Stars)
ramen <- ramen %>%
  #break down n 5 categories based on ratings
  mutate(Collection = case_when( Stars >=4.5 ~ "Premium", 
                                 Stars >=4 & Stars <4.5~"High Quality", 
                                 Stars >=3.5 & Stars <4~"Good",
                                 Stars >=3 & Stars <3.5 ~ "Average",
                                 Stars < 3 ~ "Very Low"
  ))

#grouping by collection (satr rating)
collection_summary <- ramen %>% group_by(Collection) %>% summarize( Count = n(), AvgStars = mean(Stars, na.rm =TRUE), TopCountries = paste(names(sort(table(Country), decreasing =TRUE)[1:3]), collapse =", "), TopStyles = paste(names(sort(table(Style), decreasing =TRUE)[1:2]), collapse =", "))
#printing collections summary
print(collection_summary)


#plotting Collections against stars by collection
ggplot(ramen, aes(x = Collection, y = Stars, fill = Collection)) + geom_boxplot() + labs(title = "Ramen Ratings by Collection", x ="Collection", y ="Stars") + theme_minimal() + theme(axis.text.x = element_text(angle =45, hjust =1
))


ramen %>% group_by(Collection, Country) %>% summarize(Count = n()) %>% group_by(Collection) %>% top_n(5, Count) %>% ggplot(aes(x = reorder(Country, Count), y = Count, fill = Collection)) + geom_col() + facet_wrap(~Collection, scales ="free_y") + coord_flip() + labs(title = "Top Countries in Each Ramen Collection", x ="Country", y ="Count"
)


#define a threshold
salt_threshold <- mean(ramen$perc_salt, na.rm =TRUE)
salt_threshold <-20
#filter higher than salt_threshold and equal to 5 stars
top_stars_high_salt <- ramen %>% filter(Stars == 5 & perc_salt > salt_threshold)
#top Variety with higher concentration of salt and stars rating
unique_varieties <- unique(top_stars_high_salt$Variety)
print(unique_varieties)

#summary statistics
summary_stats <- top_stars_high_salt %>% summarize( mean_salt = mean(perc_salt, na.rm =TRUE), min_salt = min(perc_salt, na.rm =TRUE), max_salt = max(perc_salt, na.rm =TRUE), count = n() )
print(summary_stats)


# Create a plot of salt percentage for the top varieties
ggplot(top_stars_high_salt, aes(x = Variety, y = perc_salt)) + geom_boxplot() + labs(title ="Salt Percentage of Top-Rated Ramen Varieties", x ="Ramen Variety", y =
                                                                                       "Percentage of Salt") + theme(axis.text.x = element_text(angle =45, hjust =1))


