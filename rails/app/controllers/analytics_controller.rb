class AnalyticsController < ApplicationController

  protect_from_forgery with: :exception
  before_filter :set_search_query
  before_filter :set_form_parameters, :only => [:index, :top_companies]

  def index
    data_internships = Internship.internship_count_by_semester(params)
    @data_internships = format_data_for_graphs(data_internships)
  end

  # Ajax request for count of internships by semester.
  def count_by_semester_request
    data_internships = Internship.internship_count_by_semester(params)
    @data_internships = format_data_for_graphs(data_internships)

    render json: {
               :data_internships => @data_internships
           }.to_json.html_safe
  end

  # Ajax request for top companies graph.
  def top_companies_request
    top_companies_data, @top_companies_total_count = Internship.top_companies(params)
    @top_companies = format_data_for_graphs(top_companies_data)

    render json: {
               :top_companies_total_count => @top_companies_total_count,
               :top_companies => @top_companies
            }.to_json.html_safe
  end

  def top_companies
    top_companies_data, @top_companies_total_count = Internship.top_companies(params)
    @top_companies = format_data_for_graphs(top_companies_data)

    render :index
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

  # Fetching data used for selects in analytics forms.
  def set_form_parameters
    @all_countries = Internship.all_countries_ordered_for_select
    @all_cities_grouped_by_countries = Internship.all_cities_grouped_by_country_for_select
    @all_levels = Internship.all_levels_for_select
    @all_branches = Internship.all_branches_for_select
  end

  # Default search parameters.
  def set_search_query
    @all_semesters = Internship.all_semesters_ordered

    # Adding missing parameters by default
    params[:from_semester] ||= @all_semesters.last()
    params[:to_semester] ||= @all_semesters.first()
  end
end