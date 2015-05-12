class AnalyticsController < ApplicationController

  protect_from_forgery with: :exception
  before_filter :set_search_query, :only => [:index, :count_by_semester_request]

  def index
    @internship_analytics = true
    @all_countries = Internship.all_countries_ordered_for_select
    data_internships = Internship.internship_count_by_semester(params)
    @data_internships = format_data_for_graphs(data_internships)
    @all_cities_grouped_by_countries = Internship.all_cities_grouped_by_country_for_select

    top_companies_data, @top_companies_total_count = Internship.top_companies(params)
    @top_companies = format_data_for_graphs(top_companies_data)
  end

  def count_by_semester_request
    @data_internships = Internship.internship_count_by_semester(params)
  end

  protected

  # data input is like this: [2010, "P", "GI"]: 53, [2010, "P", "GB"]: 58
  # data output is like this: { "P2010": {"GI": 53, "GB": 58}, "A2010": {"GI": 53, "GB": 58} }
  def format_data_for_graphs(data)
    internship_data = Hash.new

    data.each do |semester, count|
      if internship_data.has_key?(semester[1] + semester[0].to_s)
        internship_data[semester[1] + semester[0].to_s][semester[2]] = count
      else
        internship_data[semester[1] + semester[0].to_s] = { semester[2] => count }
      end
    end

    return internship_data
  end

  # Default search parameters.
  def set_search_query
    @all_semesters = Internship.all_semesters_ordered
    @internship_types = Internship.internship_types
    @all_branches = Internship.all_branches_for_select

    # Adding missing parameters by default
    params[:from_semester] ||= @all_semesters.last()
    params[:to_semester] ||= @all_semesters.first()
  end
end