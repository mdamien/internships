class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
  before_filter :set_search_query, :only => [:index]

  before_filter CASClient::Frameworks::Rails::Filter

  def index
    @internship_list = true

    @all_levels = Internship.all_levels_for_select
    @all_branches = Internship.all_branches_for_select

    #Retrieving most recent year data from database by default
    @internships = Internship.search(params).order_internships_for_table

    #Internship data values in JSON (countries, cities, companies)
    @internship_data_json = {
        "countries" => SortedSet.new,
        "cities" => SortedSet.new,
        "companies" => SortedSet.new
    }

    @internships.each do |i|
      @internship_data_json["countries"].add(i.country.titleize) unless i.country.nil?
      @internship_data_json["cities"].add(i.city.titleize) unless i.city.nil?
      @internship_data_json["companies"].add(i.company.titleize) unless i.company.nil?
    end
  end
  
  def view
    @internship = Internship.find(params[:id])
  end

  def logout
    CASClient::Frameworks::Rails::Filter.logout(self)
  end

  protected

  #Default search parameters.
  def set_search_query
    @all_semesters = Internship.all_semesters_ordered

    # Adding missing parameters by default
    params[:from_semester] ||= @all_semesters.first()
    params[:to_semester] ||= @all_semesters.first()
  end
end