class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
  before_filter :set_search_query, :only => [:index]

  def index
    #Retrieving most recent year data from database by default
    @internships = Internship.search(params)
    @years = Internship.allInternshipYears.map { |i| i.year }
  end
  
  def view
    @internship = Internship.find(params[:id])
  end

  protected

  #Default search parameters.
  def set_search_query
    most_recent_year = Internship.maximum("year")

    #Adding missing parameters by default
    params[:from_year] ||= most_recent_year
    params[:to_year] ||= most_recent_year
    params[:from_semester] ||= "P"
    params[:to_semester] ||= "A"
  end

end
