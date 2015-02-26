class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
  
  def index
    #Retrieving most recent year data from database by default
    most_recent_year = Internship.maximum("year")
    @internships = Internship.where("year = ?", most_recent_year)
                       .order(year: :ASC)
                       .order(semester: :DESC)
                       .order(country: :ASC)
                       .order(company: :ASC)
  end
  
  def view
    @internship = Internship.find(params[:id])
  end
end
