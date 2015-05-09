class AnalyticsController < ApplicationController

  protect_from_forgery with: :exception
  before_filter :set_search_query, :only => [:index, :count_by_semester_request]

  def index
    @internship_analytics = true
    @years = Internship.all_internship_years
    @data_internships = Internship.internship_count_by_semester(params)
  end

  def count_by_semester_request
    @data_internships = Internship.internship_count_by_semester(params)
  end

  protected

  #Default search parameters.
  def set_search_query
    @internship_types = Internship.internship_types
    @all_branches = Internship.all_branches_for_select
    most_recent_year = Internship.maximum("year")

    #Adding missing parameters by default
    params[:from_year] ||= most_recent_year
    params[:to_year] ||= most_recent_year
    params[:from_semester] ||= "P"
    params[:to_semester] ||= "A"
    params[:internship_type] ||= @internship_types["Tous"]
    params[:branch] ||= "Toutes"
  end
end