class AnalyticsController < ApplicationController

  protect_from_forgery with: :exception
  before_filter :set_search_query, :only => [:index, :count_by_semester_request]

  def index
    @internship_analytics = true
    @all_countries = Internship.all_countries_ordered_for_select
    @data_internships = Internship.internship_count_by_semester(params)
  end

  def count_by_semester_request
    @data_internships = Internship.internship_count_by_semester(params)
  end

  protected

  # Default search parameters.
  def set_search_query
    @all_semesters = Internship.all_semesters_ordered
    @internship_types = Internship.internship_types
    @all_branches = Internship.all_branches_for_select

    # Adding missing parameters by default
    params[:from_semester] ||= @all_semesters.first()
    params[:to_semester] ||= @all_semesters.first()
    params[:internship_type] ||= @internship_types["Tous"]
    params[:branch] ||= @all_branches.first()
  end
end