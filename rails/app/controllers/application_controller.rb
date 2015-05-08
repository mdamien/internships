class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
  before_filter :set_search_query, :only => [:index]

  before_filter CASClient::Frameworks::Rails::Filter

  def index
    @internship_list = true

    #Retrieving most recent year data from database by default
    @internships = Internship.search(params)
    @years = Internship.all_internship_years.map { |i| i.year }

    #Internship data values in JSON (countries, cities, companies)
    @internship_data_json = {
        "countries" => SortedSet.new,
        "cities" => SortedSet.new,
        "companies" => SortedSet.new
    }

    @internships.each do |i|
      @internship_data_json["countries"].add(i.country)
      @internship_data_json["cities"].add(i.city)
      @internship_data_json["companies"].add(i.company)
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
    @internship_types = Internship.internship_types
    @all_branches = Hash[Internship.all_branches.map { |id, branch| [branch["name"], id] }]
    most_recent_year = Internship.maximum("year")

    #Adding missing parameters by default
    params[:from_year] ||= most_recent_year
    params[:to_year] ||= most_recent_year
    params[:from_semester] ||= "P"
    params[:to_semester] ||= "A"
    params[:internship_type] ||= @internship_types["Tous"]
    params[:branch] ||= @internship_types["Toutes"]
  end

end